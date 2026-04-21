from fastapi import APIRouter, Response, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ...core.security import hash_password, create_access_token
from ...core.config import settings
from ...core.redis import redis_client
from ...services.user import authenticate_user, get_current_active_user, get_current_user
from ...schemas.auth import Token, UserCreate, UserResponse, UserSimple, LoginResponse
from ...models.users import User, UserScope, Scope
from ...models.parish import Parish
from ...database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_scopes(session: Session, user_id) -> list[str]:
    return session.exec(
        select(Scope.name).join(UserScope).where(UserScope.user_id == user_id)
    ).all()


@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)

    parish = session.get(Parish, user.parish_id) if user.parish_id else None

    user_scopes = get_user_scopes(session, user.id)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "parish_id": str(user.parish_id) if user.parish_id else None,
            "scopes": user_scopes,
        }
    )

    response.set_cookie(
        key=settings.TOKEN_NAME,
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60,
        path="/",
    )

    return LoginResponse(
        message=f"Bem-vindo, {user.username}!",
        parish_id=parish.id if parish else user.id,
        parish_slug=parish.slug if parish else "",
        parish_name=parish.name if parish else "",
    )


@router.get("/logout")
def logout(response: Response, user: User = Depends(get_current_active_user)):
    if not user:
        return {"message": "You're not logged in"}

    response.delete_cookie(key=settings.TOKEN_NAME, path="/")
    redis_client.delete(f"token:{user.id}")

    return {"message": "Você foi desconectado com sucesso."}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/", response_model=list[UserSimple])
def list_users(
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    return session.exec(
        select(User).where(
            User.is_active == True,
            User.parish_id == current_user.parish_id,
        )
    ).all()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    parish = session.exec(select(Parish).where(Parish.slug == user.parish_slug)).first()
    if not parish:
        raise HTTPException(status_code=404, detail="Paróquia não encontrada.")
    if not parish.is_active:
        raise HTTPException(status_code=403, detail="Paróquia inativa.")

    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já registrado.")

    data = user.model_dump()
    data["password_hash"] = hash_password(data.pop("password"))
    data.pop("parish_slug")
    data["parish_id"] = parish.id

    db_user = User(**data)
    session.add(db_user)
    session.flush()

    scope_id = session.exec(select(Scope.id).where(Scope.name == "me")).first()
    user_scope = UserScope(user_id=db_user.id, scope_id=scope_id)
    session.add(user_scope)

    session.commit()
    session.refresh(db_user)
    return db_user
