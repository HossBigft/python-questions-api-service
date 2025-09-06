from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import update, select


from app.core.security import get_password_hash, verify_password
from app.schemas import (
    UserCreate,
    UserUpdate,
)
from app.db.models import User


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User(
        email=user_create.email,
        is_active=True,
        full_name=user_create.full_name,
        is_superuser=user_create.is_superuser,
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data:
        password = user_data.pop("password")  # Remove password from user_data
        hashed_password = get_password_hash(password)
        user_data["hashed_password"] = hashed_password
    stmt = update(User).where(User.id == db_user.id).values(user_data)
    session.execute(stmt)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.execute(statement).scalar()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
