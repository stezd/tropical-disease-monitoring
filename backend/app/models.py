import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import EmailStr
from sqlalchemy import JSON, DateTime
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Anonymous screening result, saved only after the patient agrees.
# No user link, name, NIK, BPJS number, or photo.
class Screening(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    flow_id: str = Field(max_length=20, index=True)
    answers: dict[str, Any] = Field(sa_type=JSON)
    route: str = Field(max_length=10)
    unknown: bool = False
    top_disease: str | None = Field(default=None, max_length=20)
    top_score: float | None = None
    engine: str = Field(max_length=20)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class ScreeningPublic(SQLModel):
    id: uuid.UUID
    flow_id: str
    answers: dict[str, Any]
    route: str
    unknown: bool
    top_disease: str | None
    top_score: float | None
    engine: str
    created_at: datetime | None = None


class ScreeningsPublic(SQLModel):
    data: list[ScreeningPublic]
    count: int


# Verified health facility from SATUSEHAT Master Sarana Index (MSI).
# Mirrored locally to keep referral routing working offline and protect coordinates.
class Facility(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    satusehat_id: str = Field(max_length=64, unique=True, index=True)
    code: str = Field(max_length=64, index=True)
    name: str = Field(max_length=255, index=True)
    jenis_sarana_kode: str = Field(max_length=10, index=True)
    jenis_sarana_nama: str = Field(max_length=100)
    province_code: str = Field(max_length=10, index=True)
    province_name: str = Field(max_length=100, index=True)
    city_name: str | None = Field(default=None, max_length=100)
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=100)
    # Curated WhatsApp number, set by an admin (PUT /facilities/{id}/whatsapp).
    # MSI has no WhatsApp field and its `telp` is usually a landline, so this is
    # never written by the sync -- it survives re-syncs untouched.
    wa_number: str | None = Field(default=None, max_length=32)
    latitude: float | None = Field(default=None, index=True)
    longitude: float | None = Field(default=None, index=True)
    operational: bool = Field(default=True)
    status_sarana: str | None = Field(default=None, max_length=50)
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class FacilityPublic(SQLModel):
    satusehat_id: str
    code: str
    name: str
    jenis_sarana_kode: str
    jenis_sarana_nama: str
    province_code: str
    province_name: str
    city_name: str | None
    address: str | None
    phone: str | None
    # Curated mobile number for the WhatsApp button, when an admin has set one.
    wa_number: str | None = None
    # MSI data-confidence marker ("verified"/"valid"), used to break near-ties
    # when two facilities are about the same distance away.
    status_sarana: str | None = None
    latitude: float | None
    longitude: float | None


class FacilitiesPublic(SQLModel):
    data: list[FacilityPublic]
    count: int


# A facility picked by distance, with how far it is (straight-line km).
class FacilityNearestPublic(FacilityPublic):
    distance_km: float


class FacilitiesNearestPublic(SQLModel):
    data: list[FacilityNearestPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
