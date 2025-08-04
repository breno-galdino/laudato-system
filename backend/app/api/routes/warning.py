from fastapi import APIRouter, HTTPException, Security, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
import json

from ...core.redis import redis_client
from ...database import get_session
from ...models.warning import Warning as WarningModel
from ...models.users import User
from ...schemas.warning import WarningRead, WarningCreate, WarningUpdate
from ...services.user import get_current_user

router = APIRouter(prefix="/warnings", tags=["warnings"])
_cached_key = "warnings:all"

@router.get("/", response_model=list[WarningRead])
async def get_warnings(session: Session = Depends(get_session)):
    cached_data = redis_client.get(_cached_key)
    
    if cached_data:
        print("Cached Data Warning - Redis")
        return json.loads(cached_data)
    
    warnings = session.exec(select(WarningModel)).all()
    
    serialized = jsonable_encoder(warnings)

    redis_client.setex(_cached_key, 600, json.dumps(serialized))
    
    return warnings


@router.post("/", response_model=WarningRead, status_code=201)
async def create_warning(
    warning: WarningCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
        
    db_warning = WarningModel(**warning.model_dump())
    session.add(db_warning)
    session.commit()
    session.refresh(db_warning)
    
    redis_client.delete(_cached_key)
    return db_warning


@router.put("/{warning_id}", response_model=WarningRead)
async def update_warning(
    warning_id: int,
    warning: WarningUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
        
    db_warning = session.get(WarningModel, warning_id)
    if not db_warning:
        raise HTTPException(status_code=404, detail="Warning not found")
    for key, value in warning.model_dump(exclude_unset=True).items():
        setattr(db_warning, key, value)
    session.add(db_warning)
    session.commit()
    session.refresh(db_warning)
    
    redis_client.delete(_cached_key)
    return db_warning


@router.delete("/{warning_id}", status_code=204)
async def delete_warning(
    warning_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):        
    db_warning = session.get(WarningModel, warning_id)
    if not db_warning:
        raise HTTPException(status_code=404, detail="Warning not found")
    session.delete(db_warning)
    session.commit()
    
    redis_client.delete(_cached_key)
    return
