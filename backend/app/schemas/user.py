"""User schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=255)
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update schema."""

    full_name: str | None = Field(None, max_length=255)
    is_active: bool | None = None


class UserResponse(BaseModel):
    """User response schema (does not expose password_hash)."""

    id: UUID
    email: str
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserDetailResponse(UserResponse):
    """Detailed user response schema."""

    pass


class UserInDB(UserResponse):
    """User schema with password_hash (for internal use only)."""

    password_hash: str
