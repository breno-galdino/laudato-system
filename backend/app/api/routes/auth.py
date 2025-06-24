from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.security import hash_password, create_access_token
from app.services.user import authenticate_user, get_current_active_user
from app.schemas.auth import Token, UserCreate, UserResponse
from app.models.users import User, UserScope, Scope
from app.database import get_session

router = APIRouter()

def get_user_scopes(session: Session, user_id: int) -> list[str]:
    result = session.exec(
        select(Scope.name).join(UserScope).where(UserScope.user_id == user_id)
    ).all()
    return result

@router.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    user_scopes = get_user_scopes(session, user.id)
    access_token = create_access_token(data={"sub": str(user.id),"username": user.username,"email": user.email, "scopes": user_scopes})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já registrado")
    data = user.model_dump()
    data["password_hash"] = hash_password(data.pop("password"))
    db_user = User(**data)
    user_scope = UserScope(user_id=db_user.id, scope_name="me")
    session.add(db_user)
    session.add(user_scope)
    session.commit()
    session.refresh(db_user)
    return db_user
