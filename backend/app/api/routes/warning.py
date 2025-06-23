from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from ...database import get_session
from ...models.warning import Warning as WarningModel
from ...schemas.warning import WarningRead, WarningCreate, WarningUpdate

router = APIRouter(prefix="/warnings", tags=["warnings"])

@router.get("/", response_model=list[WarningRead])
async def get_warnings(session: Session = Depends(get_session)):
    return session.exec(select(WarningModel)).all()

@router.post("/", response_model=WarningRead, status_code=201)
async def create_warning(warning: WarningCreate, session: Session = Depends(get_session)):
    db_warning = WarningModel(**warning.dict())
    session.add(db_warning)
    session.commit()
    session.refresh(db_warning)
    return db_warning

@router.put("/{warning_id}", response_model=WarningRead)
async def update_warning(warning_id: int, warning: WarningUpdate, session: Session = Depends(get_session)):
    db_warning = session.get(WarningModel, warning_id)
    if not db_warning:
        raise HTTPException(status_code=404, detail="Warning not found")
    for key, value in warning.model_dump(exclude_unset=True).items():
        setattr(db_warning, key, value)
    session.add(db_warning)
    session.commit()
    session.refresh(db_warning)
    return db_warning

@router.delete("/{warning_id}", status_code=204)
async def delete_warning(warning_id: int, session: Session = Depends(get_session)):
    db_warning = session.get(WarningModel, warning_id)
    if not db_warning:
        raise HTTPException(status_code=404, detail="Warning not found")
    session.delete(db_warning)
    session.commit()
    return