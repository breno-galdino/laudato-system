from fastapi import APIRouter, HTTPException, Depends, Security, Query
from sqlmodel import Session, select
import json

from ...database import get_session
from ...core.redis import redis_client
from ...models.category import Category as CategoryModel
from ...models.parish import Parish
from ...models.users import User
from ...schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from ...services.user import get_current_user

router = APIRouter(prefix="/category", tags=["category"])


def _cache_key(parish_id) -> str:
    return f"categories:{parish_id}"


@router.get("/", response_model=list[CategoryRead])
def get_categories(
    parish_slug: str = Query(..., description="Slug da paróquia"),
    session: Session = Depends(get_session),
):
    parish = session.exec(select(Parish).where(Parish.slug == parish_slug)).first()
    if not parish:
        raise HTTPException(status_code=404, detail="Paróquia não encontrada.")

    key = _cache_key(parish.id)
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    categories = session.exec(
        select(CategoryModel).where(CategoryModel.parish_id == parish.id)
    ).all()

    redis_client.setex(key, 600, json.dumps([c.model_dump() for c in categories], default=str))
    return categories


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_category = CategoryModel(**category.model_dump(), parish_id=current_user.parish_id)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_category = session.get(CategoryModel, category_id)
    if not db_category or db_category.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)

    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_category


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_category = session.get(CategoryModel, category_id)
    if not db_category or db_category.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")

    session.delete(db_category)
    session.commit()
    redis_client.delete(_cache_key(current_user.parish_id))
