import uuid
from datetime import UTC, date, datetime
from typing import Any

from pydantic import EmailStr
from sqlalchemy import JSON, Date, DateTime
from sqlmodel import Field, Relationship, SQLModel


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
    # Google account ("sub" claim) linked to this user; null = never linked.
    google_sub: str | None = Field(
        default=None, unique=True, index=True, max_length=255
    )
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    # Deleting an account deletes its saved screenings too.
    screenings: list[Screening] = Relationship(
        back_populates="user", cascade_delete=True
    )


# Sign in with a Google ID token from Google Identity Services.
class GoogleLogin(SQLModel):
    credential: str = Field(min_length=1)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Screening result, saved only after the patient agrees.
# Linked to the account when a signed-in user saves it.
# No name, NIK, BPJS number, or photo.
class Screening(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID | None = Field(
        default=None, foreign_key="user.id", ondelete="CASCADE", index=True
    )
    user: User | None = Relationship(back_populates="screenings")
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


# One row in the signed-in user's history. No raw answers.
class ScreeningHistoryItem(SQLModel):
    id: uuid.UUID
    flow_id: str
    route: str
    unknown: bool
    top_disease: str | None
    top_score: float | None
    created_at: datetime | None = None


class ScreeningsHistoryPublic(SQLModel):
    data: list[ScreeningHistoryItem]
    count: int


# One finished screening as statistics, without direct identity. Guests included.
# NO user id, email, IP, created_at, exact age, raw vitals, drug text, or coordinates:
# the whitelist lives in app/domain/screening_stat.py. Not deleted with an account
# because it is linked to no one.
class ScreeningStat(SQLModel, table=True):
    __tablename__ = "screening_stat"

    # Random id of one quiz run (made in the browser), only to avoid double counting.
    event_id: uuid.UUID = Field(primary_key=True)
    day: date = Field(sa_type=Date, index=True)
    flow_id: str = Field(max_length=20)
    route: str = Field(max_length=10)
    unknown: bool = False
    top_disease: str | None = Field(default=None, max_length=20)
    top_score: float | None = None
    others: list[str] = Field(default_factory=list, sa_type=JSON)
    engine: str = Field(max_length=20)
    who: str | None = Field(default=None, max_length=30)
    sex: str | None = Field(default=None, max_length=1)
    age_band: str | None = Field(default=None, max_length=5)
    pregnant: bool | None = None
    province: str | None = Field(default=None, max_length=64)
    complaint: str | None = Field(default=None, max_length=30)
    pattern: str | None = Field(default=None, max_length=30)
    red_flags: list[str] = Field(default_factory=list, sa_type=JSON)
    companion: list[str] = Field(default_factory=list, sa_type=JSON)
    eco: list[str] = Field(default_factory=list, sa_type=JSON)
    body: list[str] = Field(default_factory=list, sa_type=JSON)
    vital_proxy: list[str] = Field(default_factory=list, sa_type=JSON)
    nutrition_proxy: str | None = Field(default=None, max_length=10)
    pain: int | None = None
    temp_cat: str | None = Field(default=None, max_length=15)
    bp_cat: str | None = Field(default=None, max_length=15)
    glucose_high: bool = False
    bmi_cat: str | None = Field(default=None, max_length=10)
    no_thermo: bool = False
    no_bp: bool = False
    drugs_given: bool = False


# One group of the stats summary. `count` is None when the group is below k.
class ScreeningStatRow(SQLModel):
    period: date
    province: str | None
    disease: str | None
    route: str
    count: int | None


class ScreeningStatSummary(SQLModel):
    data: list[ScreeningStatRow]
    k: int


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
