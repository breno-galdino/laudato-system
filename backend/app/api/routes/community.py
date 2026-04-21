from fastapi import APIRouter, Depends, HTTPException, Security
from sqlmodel import Session, select
from datetime import datetime, timezone

from ...models.community import Community
from ...models.users import User
from ...schemas.community import CommunityCreate, CommunityRead, CommunityUpdate
from ...services.user import get_current_active_user, get_current_user
from ...database import get_session

router = APIRouter(prefix="/community", tags=["community"])


@router.get("/", response_model=list[CommunityRead])
def list_communities(
    type: str | None = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    query = select(Community).where(
        Community.parish_id == current_user.parish_id,
        Community.is_active == True,
    )
    if type:
        query = query.where(Community.type == type)
    query = query.order_by(Community.name)
    return session.exec(query).all()


@router.post("/", response_model=CommunityRead)
def create_community(
    payload: CommunityCreate,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    session: Session = Depends(get_session),
):
    community = Community(**payload.model_dump(), parish_id=current_user.parish_id)
    session.add(community)
    session.commit()
    session.refresh(community)
    return community


@router.get("/{community_id}", response_model=CommunityRead)
def get_community(
    community_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    community = session.get(Community, community_id)
    if not community or community.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Comunidade não encontrada.")
    return community


@router.patch("/{community_id}", response_model=CommunityRead)
def update_community(
    community_id: int,
    payload: CommunityUpdate,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    session: Session = Depends(get_session),
):
    community = session.get(Community, community_id)
    if not community or community.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Comunidade não encontrada.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(community, field, value)
    community.updated_at = datetime.now(timezone.utc)
    session.add(community)
    session.commit()
    session.refresh(community)
    return community


@router.delete("/{community_id}")
def delete_community(
    community_id: int,
    current_user: User = Security(get_current_user, scopes=["admin"]),
    session: Session = Depends(get_session),
):
    community = session.get(Community, community_id)
    if not community or community.parish_id != current_user.parish_id:
        raise HTTPException(status_code=404, detail="Comunidade não encontrada.")
    community.is_active = False
    community.updated_at = datetime.now(timezone.utc)
    session.add(community)
    session.commit()
    return {"message": "Comunidade desativada."}
