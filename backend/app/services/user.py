from fastapi import Depends, HTTPException, HTTPException, Security, status, Request
from fastapi.security import SecurityScopes
from pydantic import ValidationError
from typing import Annotated
from jose import JWTError
from sqlmodel import Session, select
import json

from ..database import get_session, engine
from ..core.security import verify_password
from ..core.redis import redis_client
from ..core.config import settings
from ..services.auth import decode_token
from ..models.users import User, Scope
from ..schemas.auth import TokenData


def load_scopes_from_db() -> dict:
    with Session(engine) as session:
        scopes = session.exec(select(Scope)).all()
        return {s.name: s.description for s in scopes}


scopes = load_scopes_from_db()


def get_user(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()


def authenticate_user(session: Session, email: str, password: str) -> User:
    user = get_user(session, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    request: Request,
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(request, settings.TOKEN_NAME)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(
            id=user_id,
            parish_id=payload.get("parish_id"),
            scopes=token_scopes,
        )
    except (JWTError, ValidationError):
        raise credentials_exception
    
    cached_data = redis_client.get(f"token:{user_id}")
    if cached_data:
        print("Cached Data User - Redis")
        user_data = json.loads(cached_data)
        return User.model_validate(user_data)
    
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    
    redis_client.setex(
        f"token:{user_id}", 3600, json.dumps(user.model_dump(), default=str)
    )
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
