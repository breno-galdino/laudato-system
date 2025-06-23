from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ...core.security import hash_password, create_access_token, create_refresh_token
from ...services.user import authenticate_user
from ...models.users import User as UserModel
from ...schemas.auth import UserCreate, UserResponse
from ...schemas.auth import Token
from ...database import get_session

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(UserModel).where(UserModel.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já registrado")


    data = user.model_dump()
    data["password_hash"] = hash_password(data.pop("password"))

    db_user = UserModel(**data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
