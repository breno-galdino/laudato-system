from sqlmodel import Session, select
from ..models.users import User
from typing import Optional

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()
