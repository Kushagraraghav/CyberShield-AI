"""Authentication service."""

from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import UserRegister


def get_user_by_email(db: Session, email: str) -> User | None:
    """Find a user by email."""
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def get_user_by_username(db: Session, username: str) -> User | None:
    """Find a user by username."""
    statement = select(User).where(User.username == username)
    return db.scalar(statement)


def get_user_by_identifier(db: Session, identifier: str) -> User | None:
    """Find a user by username or email."""
    statement = select(User).where(
        or_(
            User.username == identifier,
            User.email == identifier,
        )
    )
    return db.scalar(statement)


def register_user(db: Session, user_data: UserRegister) -> User:
    """Create a new user."""

    existing_user = db.scalar(
        select(User).where(
            or_(
                User.email == user_data.email,
                User.username == user_data.username,
            )
        )
    )

    if existing_user:
        if existing_user.email == user_data.email:
            raise ValueError("Email already registered")

        raise ValueError("Username already registered")

    user = User(
        id=uuid4(),
        email=str(user_data.email),
        username=user_data.username,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password),
        is_active=True,
        is_superuser=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    identifier: str,
    password: str,
) -> User | None:
    """Authenticate a user using username/email and password."""

    user = get_user_by_identifier(db, identifier)

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def create_user_token(user: User) -> str:
    """Create an access token for a user."""

    return create_access_token(
        subject=str(user.id),
        additional_claims={
            "username": user.username,
            "is_superuser": user.is_superuser,
        },
    )
