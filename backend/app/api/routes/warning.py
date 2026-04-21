from fastapi import APIRouter, HTTPException, Security, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
import json

from ...core.redis import redis_client
from ...database import get_session
from ...models.warning import Warning as WarningModel
from ...models.parish import Parish
from ...models.users import User
from ...schemas.warning import WarningRead, WarningCreate, WarningUpdate
from ...services.user import get_current_user

router = APIRouter(prefix="/warnings", tags=["warnings"])


def _cache_key(parish_id) -> str:
    return f"warnings:{parish_id}"


@router.get("/", response_model=list[WarningRead])
async def get_warnings(
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

    warnings = session.exec(
        select(WarningModel).where(WarningModel.parish_id == parish.id)
    ).all()

    redis_client.setex(key, 600, json.dumps(jsonable_encoder(warnings)))
    return warnings


@router.post("/", response_model=WarningRead, status_code=201)
async def create_warning(
    warning: WarningCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_warning = WarningModel(**warning.model_dump(), parish_id=current_user.parish_id)
    session.add(db_warning)
    session.commit()
    session.refresh(db_warning)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_warning


@router.put("/{warning_id}", response_model=WarningRead)
async def update_warning(
    warning_id: int,
    warning: WarningUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_warning = session.get(WarningModel, warning_id)
    if not db_warning or db_warning.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Aviso não encontrado.")

    for key, value in warning.model_dump(exclude_unset=True).items():
        setattr(db_warning, key, value)

    session.add(db_warning)
    session.commit()
    session.refresh(db_warning)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_warning


@router.delete("/{warning_id}", status_code=204)
async def delete_warning(
    warning_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_warning = session.get(WarningModel, warning_id)
    if not db_warning or db_warning.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Aviso não encontrado.")

    session.delete(db_warning)
    session.commit()
    redis_client.delete(_cache_key(current_user.parish_id))
