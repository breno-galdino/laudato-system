from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select
import json

from ...database import get_session

from ...core.redis import redis_client
from ...models.celebration import Celebration as CelebrationModel, Role, Assignment
from ...models.users import User
from ...schemas.celebration import CelebrationCreate, CelebrationRead, CelebrationUpdate, AssignmentRole
from ...services.user import get_current_user

router = APIRouter(prefix="/celebration", tags=["celebration"])
_cache_key = "celebration:all"

@router.get("/", response_model=list[CelebrationRead])
def get_celebrations(session: Session = Depends(get_session)):    
    cached_data = redis_client.get(_cache_key)
    if cached_data:
        print("Cached Data Celebration - Redis")
        return json.loads(cached_data)
    
    celebrations = session.exec(select(CelebrationModel)).all()
    
    serialized = jsonable_encoder(celebrations)

    redis_client.setex(_cache_key, 600, json.dumps(serialized))
    
    return celebrations


@router.post("/", response_model=CelebrationRead, status_code=201)
def create_celebration(
    celebration: CelebrationCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_celebration = CelebrationModel(**celebration.model_dump())
    session.add(db_celebration)
    session.commit()
    session.refresh(db_celebration)
    
    redis_client.delete(_cache_key)
    return db_celebration

@router.post("/assign", response_model=list[Assignment], status_code=201)
def create_assignments(
    celebration_id: int,
    assignments: list[AssignmentRole],
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    created_assignments = []

    for assignment in assignments:
        assignment = AssignmentRole.model_validate(assignment)
        assignment = assignment.model_dump()
        user_id = assignment['user_id']
        role_id = assignment['role_id']

        existing = session.exec(
            select(Assignment).where(
                Assignment.celebration_id == celebration_id,
                Assignment.user_id == user_id,
                Assignment.role_id == role_id
            )
        ).first()

        if existing:
            continue

        new_assignment = Assignment(
            celebration_id=celebration_id,
            user_id=user_id,
            role_id=role_id
        )
        session.add(new_assignment)
        created_assignments.append(new_assignment)

    session.commit()

    # refresh todos os criados
    for assignment in created_assignments:
        session.refresh(assignment)

    return created_assignments

@router.put("/{celebration_id}", response_model=CelebrationRead)
def update_category(
    celebration_id: int,
    celebration: CelebrationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_current_user, scopes=["admin"]),
):
    db_celebration = session.get(CelebrationModel, celebration_id)
    if not db_celebration:
        raise HTTPException(status_code=404, detail="Celebration not found")

    for key, value in celebration.model_dump(exclude_unset=True).items():
        setattr(db_celebration, key, value)

    session.add(db_celebration)
    session.commit()
    session.refresh(db_celebration)
    
    redis_client.delete(_cache_key)
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
    
    redis_client.delete(_cache_key)
    return
