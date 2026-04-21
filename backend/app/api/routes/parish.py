from fastapi import APIRouter, HTTPException, Depends, Security
from sqlmodel import Session, select

from ...database import get_session
from ...core.security import hash_password
from ...models.parish import Parish
from ...models.users import User, UserScope, Scope
from ...schemas.parish import ParishCreate, ParishRead, ParishUpdate, ParishRegister
from ...schemas.auth import UserResponse
from ...services.user import get_current_user

router = APIRouter(prefix="/parish", tags=["parish"])


@router.get("/", response_model=list[ParishRead])
def list_parishes(session: Session = Depends(get_session)):
    """Lista todas as paróquias ativas (público)."""
    return session.exec(select(Parish).where(Parish.is_active == True)).all()


@router.post("/register", status_code=201)
def register_parish(payload: ParishRegister, session: Session = Depends(get_session)):
    """Cria uma nova paróquia e seu primeiro usuário admin."""

    if session.exec(select(Parish).where(Parish.slug == payload.parish.slug)).first():
        raise HTTPException(status_code=400, detail="Slug já em uso.")

    if session.exec(select(User).where(User.email == payload.admin_email)).first():
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    parish = Parish(**payload.parish.model_dump())
    session.add(parish)
    session.flush()

    admin_user = User(
        parish_id=parish.id,
        full_name=payload.admin_full_name,
        email=payload.admin_email,
        username=payload.admin_username,
        password_hash=hash_password(payload.admin_password),
    )
    session.add(admin_user)
    session.flush()

    admin_scope = session.exec(select(Scope).where(Scope.name == "admin")).first()
    me_scope = session.exec(select(Scope).where(Scope.name == "me")).first()

    if admin_scope:
        session.add(UserScope(user_id=admin_user.id, scope_id=admin_scope.id))
    if me_scope:
        session.add(UserScope(user_id=admin_user.id, scope_id=me_scope.id))

    session.commit()
    session.refresh(parish)
    session.refresh(admin_user)

    return {
        "parish": ParishRead.model_validate(parish),
        "admin": UserResponse.model_validate(admin_user),
    }


@router.get("/me", response_model=ParishRead)
def get_my_parish(
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["me"]),
):
    if not current_user.parish_id:
        raise HTTPException(status_code=404, detail="Usuário sem paróquia associada.")
    parish = session.get(Parish, current_user.parish_id)
    if not parish:
        raise HTTPException(status_code=404, detail="Paróquia não encontrada.")
    return parish


@router.put("/me", response_model=ParishRead)
def update_my_parish(
    data: ParishUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    parish = session.get(Parish, current_user.parish_id)
    if not parish:
        raise HTTPException(status_code=404, detail="Paróquia não encontrada.")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(parish, key, value)

    session.add(parish)
    session.commit()
    session.refresh(parish)
    return parish
