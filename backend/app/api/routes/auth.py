from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ...core.security import hash_password, verify_password, create_access_token, create_refresh_token
from ...services.user import get_user_by_email
from ...models.users import User
from ...schemas.auth import Token, UserCreate
from ...database import get_session

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já registrado")

    db_user = User(email=user.email, hashed_password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"message": "Usuário criado"}
