from fastapi import APIRouter, HTTPException, Depends, Security, status
from sqlmodel import Session, select

from ...database import get_session

from ...models.category import Category as CategoryModel
from ...models.users import User
from ...schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from ...services.user import get_current_user

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/", response_model=list[CategoryRead])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(CategoryModel)).all()


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create categories."
        )
    db_category = CategoryModel(**category.model_dump())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update categories."
        )
    db_category = session.get(CategoryModel, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)

    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete categories."
        )
        
    db_category = session.get(CategoryModel, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    session.delete(db_category)
    session.commit()
    return 
