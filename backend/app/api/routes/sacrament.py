from fastapi import APIRouter, HTTPException, Security, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
import json

from ...core.redis import redis_client
from ...database import get_session
from ...models.sacrament import Sacrament as SacramentModel
from ...models.parish import Parish
from ...models.users import User
from ...schemas.sacrament import SacramentRead, SacramentCreate, SacramentUpdate, SACRAMENT_TYPES
from ...services.user import get_current_user

router = APIRouter(prefix="/sacraments", tags=["sacraments"])


def _cache_key(parish_id) -> str:
    return f"sacraments:{parish_id}"


@router.get("/types")
def get_sacrament_types():
    return SACRAMENT_TYPES


@router.get("/", response_model=list[SacramentRead])
async def get_sacraments(
    sacrament_type: str | None = Query(None, description="Filtrar por tipo"),
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    key = _cache_key(current_user.parish_id)
    if not sacrament_type:
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)

    stmt = select(SacramentModel).where(SacramentModel.parish_id == current_user.parish_id)
    if sacrament_type:
        stmt = stmt.where(SacramentModel.sacrament_type == sacrament_type)

    sacraments = session.exec(stmt).all()

    if not sacrament_type:
        redis_client.setex(key, 600, json.dumps(jsonable_encoder(sacraments)))

    return sacraments


@router.post("/", response_model=SacramentRead, status_code=201)
async def create_sacrament(
    sacrament: SacramentCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    if sacrament.sacrament_type not in SACRAMENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Tipo inválido. Opções: {', '.join(SACRAMENT_TYPES)}")

    db_sacrament = SacramentModel(**sacrament.model_dump(), parish_id=current_user.parish_id)
    session.add(db_sacrament)
    session.commit()
    session.refresh(db_sacrament)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_sacrament


@router.get("/{sacrament_id}", response_model=SacramentRead)
async def get_sacrament(
    sacrament_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_sacrament = session.get(SacramentModel, sacrament_id)
    if not db_sacrament or db_sacrament.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Sacramento não encontrado.")
    return db_sacrament


@router.put("/{sacrament_id}", response_model=SacramentRead)
async def update_sacrament(
    sacrament_id: int,
    sacrament: SacramentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_sacrament = session.get(SacramentModel, sacrament_id)
    if not db_sacrament or db_sacrament.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Sacramento não encontrado.")

    for key, value in sacrament.model_dump(exclude_unset=True).items():
        setattr(db_sacrament, key, value)

    from datetime import datetime
    db_sacrament.updated_at = datetime.utcnow()

    session.add(db_sacrament)
    session.commit()
    session.refresh(db_sacrament)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_sacrament


@router.delete("/{sacrament_id}", status_code=204)
async def delete_sacrament(
    sacrament_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_sacrament = session.get(SacramentModel, sacrament_id)
    if not db_sacrament or db_sacrament.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Sacramento não encontrado.")

    session.delete(db_sacrament)
    session.commit()
    redis_client.delete(_cache_key(current_user.parish_id))
