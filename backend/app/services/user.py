from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from jose import jwt, JWTError
from typing import Dict, Any

from app.core.config import settings
from app.models.users import User
from app.database import get_session
from app.core.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    payload = decode_token(token)
    
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido ou corrompido")

    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

def authenticate_user(session: Session, email: str, password: str) -> User:
    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return user

