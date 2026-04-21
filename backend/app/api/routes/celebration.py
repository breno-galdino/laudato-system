from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
import json

from ...database import get_session
from ...core.redis import redis_client
from ...models.celebration import Celebration as CelebrationModel, Role, Assignment
from ...models.users import User
from ...schemas.celebration import (
    CelebrationCreate,
    CelebrationRead,
    CelebrationUpdate,
    CelebrationReadFull,
    AssignmentDetail,
    AssignmentRole,
    RoleRead,
)
from ...services.user import get_current_user
from fastapi import Query
from ...models.parish import Parish

router = APIRouter(prefix="/celebration", tags=["celebration"])


def _cache_key(parish_id) -> str:
    return f"celebration:{parish_id}"


def _build_celebrations_full(session: Session, parish_id) -> list[CelebrationReadFull]:
    celebrations = session.exec(
        select(CelebrationModel).where(CelebrationModel.parish_id == parish_id)
    ).all()
    result = []
    for cel in celebrations:
        rows = session.exec(
            select(Assignment, User, Role)
            .join(User, Assignment.user_id == User.id)
            .join(Role, Assignment.role_id == Role.id)
            .where(Assignment.celebration_id == cel.id)
        ).all()
        assignments = [
            AssignmentDetail(
                id=a.id,
                user_id=a.user_id,
                user_name=u.username,
                role_id=a.role_id,
                role_name=r.name,
            )
            for a, u, r in rows
        ]
        result.append(
            CelebrationReadFull(
                id=cel.id,
                date=cel.date,
                description=cel.description,
                assignments=assignments,
            )
        )
    return result


@router.get("/public", response_model=list[CelebrationReadFull])
def get_celebrations_public(
    parish_slug: str = Query(..., description="Slug da paróquia"),
    session: Session = Depends(get_session),
):
    """Retorna celebrações futuras de uma paróquia (público)."""
    from datetime import datetime
    parish = session.exec(select(Parish).where(Parish.slug == parish_slug)).first()
    if not parish:
        raise HTTPException(status_code=404, detail="Paróquia não encontrada.")

    celebrations = session.exec(
        select(CelebrationModel)
        .where(
            CelebrationModel.parish_id == parish.id,
            CelebrationModel.date >= datetime.utcnow(),
        )
        .order_by(CelebrationModel.date)
    ).all()

    result = []
    for cel in celebrations:
        rows = session.exec(
            select(Assignment, User, Role)
            .join(User, Assignment.user_id == User.id)
            .join(Role, Assignment.role_id == Role.id)
            .where(Assignment.celebration_id == cel.id)
        ).all()
        assignments = [
            AssignmentDetail(
                id=a.id,
                user_id=a.user_id,
                user_name=u.username,
                role_id=a.role_id,
                role_name=r.name,
            )
            for a, u, r in rows
        ]
        result.append(
            CelebrationReadFull(
                id=cel.id,
                date=cel.date,
                description=cel.description,
                assignments=assignments,
            )
        )
    return result


@router.get("/", response_model=list[CelebrationReadFull])
def get_celebrations(
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["me"]),
):
    key = _cache_key(current_user.parish_id)
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)

    result = _build_celebrations_full(session, current_user.parish_id)
    serialized = jsonable_encoder(result)
    redis_client.setex(key, 600, json.dumps(serialized))
    return result


@router.get("/roles/", response_model=list[RoleRead])
def get_roles(
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["me"]),
):
    return session.exec(
        select(Role).where(Role.parish_id == current_user.parish_id)
    ).all()


@router.post("/", response_model=CelebrationRead, status_code=201)
def create_celebration(
    celebration: CelebrationCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_celebration = CelebrationModel(**celebration.model_dump(), parish_id=current_user.parish_id)
    session.add(db_celebration)
    session.commit()
    session.refresh(db_celebration)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_celebration


@router.post("/assign", response_model=list[AssignmentDetail], status_code=201)
def create_assignments(
    celebration_id: int,
    assignments: list[AssignmentRole],
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    created = []
    for item in assignments:
        item = AssignmentRole.model_validate(item)
        existing = session.exec(
            select(Assignment).where(
                Assignment.celebration_id == celebration_id,
                Assignment.user_id == item.user_id,
                Assignment.role_id == item.role_id,
            )
        ).first()
        if existing:
            continue
        new_assignment = Assignment(
            celebration_id=celebration_id,
            user_id=item.user_id,
            role_id=item.role_id,
        )
        session.add(new_assignment)
        created.append(new_assignment)

    session.commit()
    for a in created:
        session.refresh(a)

    result = []
    for a in created:
        user = session.get(User, a.user_id)
        role = session.get(Role, a.role_id)
        result.append(
            AssignmentDetail(
                id=a.id,
                user_id=a.user_id,
                user_name=user.username if user else "",
                role_id=a.role_id,
                role_name=role.name if role else "",
            )
        )

    redis_client.delete(_cache_key(current_user.parish_id))
    return result


@router.delete("/assign/{assignment_id}", status_code=204)
def delete_assignment(
    assignment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    assignment = session.get(Assignment, assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    session.delete(assignment)
    session.commit()
    redis_client.delete(_cache_key(current_user.parish_id))


@router.put("/{celebration_id}", response_model=CelebrationRead)
def update_celebration(
    celebration_id: int,
    celebration: CelebrationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_celebration = session.get(CelebrationModel, celebration_id)
    if not db_celebration or db_celebration.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Celebration not found")

    for key, value in celebration.model_dump(exclude_unset=True).items():
        setattr(db_celebration, key, value)

    session.add(db_celebration)
    session.commit()
    session.refresh(db_celebration)
    redis_client.delete(_cache_key(current_user.parish_id))
    return db_celebration


@router.delete("/{celebration_id}", status_code=204)
def delete_celebration(
    celebration_id: int,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_celebration = session.get(CelebrationModel, celebration_id)
    if not db_celebration:
        raise HTTPException(status_code=404, detail="Celebration not found")

    session.delete(db_celebration)
    session.commit()
    redis_client.delete(_cache_key(current_user.parish_id))
