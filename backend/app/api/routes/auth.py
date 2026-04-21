from fastapi import APIRouter, Response, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ...core.security import hash_password, create_access_token
from ...core.config import settings
from ...core.redis import redis_client
from ...services.user import authenticate_user, get_current_active_user, get_current_user
from ...schemas.auth import Token, UserCreate, UserResponse, UserUpdate, UserSimple, LoginResponse
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
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    scopes = get_user_scopes(session, current_user.id)
    return UserResponse.model_validate({
        **current_user.model_dump(),
        "scopes": scopes,
    })


@router.patch("/me", response_model=UserResponse)
async def update_me(
    payload: UserUpdate,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if payload.email and payload.email != current_user.email:
        conflict = session.exec(select(User).where(User.email == payload.email)).first()
        if conflict:
            raise HTTPException(status_code=400, detail="Email já em uso.")
    if payload.username and payload.username != current_user.username:
        conflict = session.exec(select(User).where(User.username == payload.username)).first()
        if conflict:
            raise HTTPException(status_code=400, detail="Nome de usuário já em uso.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    from datetime import datetime, timezone
    current_user.updated_at = datetime.now(timezone.utc)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    scopes = get_user_scopes(session, current_user.id)
    return UserResponse.model_validate({**current_user.model_dump(), "scopes": scopes})


@router.post("/switch-parish", response_model=LoginResponse)
async def switch_parish(
    response: Response,
    parish_slug: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    parish = session.exec(select(Parish).where(Parish.slug == parish_slug)).first()
    if not parish:
        raise HTTPException(status_code=404, detail="Paróquia não encontrada.")
    if not parish.is_active:
        raise HTTPException(status_code=403, detail="Paróquia inativa.")

    current_user.parish_id = parish.id
    from datetime import datetime, timezone
    current_user.updated_at = datetime.now(timezone.utc)
    session.add(current_user)
    session.commit()

    user_scopes = get_user_scopes(session, current_user.id)
    access_token = create_access_token(
        data={
            "sub": str(current_user.id),
            "parish_id": str(parish.id),
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
        message="Paróquia alterada com sucesso.",
        parish_id=parish.id,
        parish_slug=parish.slug,
        parish_name=parish.name,
    )


@router.get("/users/", response_model=list[UserSimple])
def list_users(
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    users = session.exec(
        select(User).where(
            User.parish_id == current_user.parish_id,
        ).order_by(User.created_at)
    ).all()
    result = []
    for u in users:
        scopes = get_user_scopes(session, u.id)
        result.append(UserSimple.model_validate({**u.model_dump(), "scopes": scopes}))
    return result


@router.post("/users/{user_id}/scopes/{scope_name}")
def add_user_scope(
    user_id: str,
    scope_name: str,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    from uuid import UUID as UUIDType
    target = session.get(User, UUIDType(user_id))
    if not target or target.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if scope_name not in ("admin", "minister", "me"):
        raise HTTPException(status_code=400, detail="Scope inválido.")

    scope = session.exec(select(Scope).where(Scope.name == scope_name)).first()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope não encontrado.")

    existing = session.get(UserScope, (UUIDType(user_id), scope.id))
    if not existing:
        session.add(UserScope(user_id=UUIDType(user_id), scope_id=scope.id))
        session.commit()
    return {"message": f"Scope '{scope_name}' adicionado."}


@router.delete("/users/{user_id}/scopes/{scope_name}")
def remove_user_scope(
    user_id: str,
    scope_name: str,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    from uuid import UUID as UUIDType
    # Impede admin de remover o próprio scope admin
    if UUIDType(user_id) == current_user.id and scope_name == "admin":
        raise HTTPException(status_code=400, detail="Você não pode remover seu próprio acesso de admin.")

    scope = session.exec(select(Scope).where(Scope.name == scope_name)).first()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope não encontrado.")

    user_scope = session.get(UserScope, (UUIDType(user_id), scope.id))
    if user_scope:
        session.delete(user_scope)
        session.commit()
    return {"message": f"Scope '{scope_name}' removido."}


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
