from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ...database import get_session
from ...models.diocese import Diocese
from ...schemas.diocese import DioceseRead, DioceseCreate

router = APIRouter(prefix="/diocese", tags=["diocese"])


@router.get("/", response_model=list[DioceseRead])
def list_dioceses(session: Session = Depends(get_session)):
    """Lista todas as dioceses (público)."""
    return session.exec(select(Diocese).order_by(Diocese.state, Diocese.name)).all()


@router.post("/", response_model=DioceseRead, status_code=201)
def create_diocese(data: DioceseCreate, session: Session = Depends(get_session)):
    """Cria uma diocese (uso interno / seed)."""
    diocese = Diocese(**data.model_dump())
    session.add(diocese)
    session.commit()
    session.refresh(diocese)
    return diocese
