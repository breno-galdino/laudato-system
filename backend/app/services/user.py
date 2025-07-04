from fastapi import Depends, HTTPException, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import ValidationError
from typing import Annotated
from jose import JWTError

from sqlmodel import Session, select
from ..database import get_session, engine
from ..models.users import User, Scope
from ..core.security import verify_password
from ..services.auth import decode_token
from ..schemas.auth import TokenData


def load_scopes_from_db() -> dict:
    with Session(engine) as session:
        scopes = session.exec(select(Scope)).all()
        return {s.name: s.description for s in scopes}


scopes = load_scopes_from_db()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes=scopes,
)


def get_user(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()


def authenticate_user(session: Session, email: str, password: str) -> User:
    user = get_user(session, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = decode_token(token)
        email = payload.get("email")
        username = payload.get("username")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(session, email=email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
