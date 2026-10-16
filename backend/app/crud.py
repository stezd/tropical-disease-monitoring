import secrets
import uuid
from typing import Any

from sqlmodel import Session, col, func, select

from app.core.security import get_password_hash, verify_password
from app.models import Screening, User, UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_or_create_external_user(
    *, session: Session, sub: str, email: str, full_name: str | None
) -> User:
    """User for a Google identity. Matched by `sub`, then by verified email.

    Why `google_sub`: /users/signup does not verify email, so an attacker could
    pre-register victim@gmail.com with a password they know, wait for the victim
    to sign in with Google, then log in with that password and read the victim's
    saved screenings. So:

    1. A user already linked to this `sub` is returned as is.
    2. An existing account with the same email but no `google_sub` is linked
       now (first link): `google_sub` is set and its password hash is replaced
       with a fresh random one, so any password set before the link stops
       working. The real owner can use "forgot password" (email) to set a new
       one. Existing screenings are kept: they can only have been saved by
       whoever held the account, and a pre-registered account cannot contain
       the victim's data.
    3. An account already linked to a different `sub` is refused (ValueError).
    4. Otherwise a new account is created with a random password nobody knows.
    """
    user = session.exec(select(User).where(User.google_sub == sub)).first()
    if user:
        return user
    user = get_user_by_email(session=session, email=email)
    if user:
        if user.google_sub is not None:
            raise ValueError("Email already linked to another Google account")
        user.google_sub = sub
        user.hashed_password = get_password_hash(secrets.token_urlsafe(32))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    db_obj = User(
        email=email,
        google_sub=sub,
        full_name=full_name[:255] if full_name else None,
        hashed_password=get_password_hash(secrets.token_urlsafe(32)),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_screenings(
    *, session: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> tuple[list[Screening], int]:
    """A user's saved screenings, newest first, with the total count."""
    count_statement = (
        select(func.count()).select_from(Screening).where(Screening.user_id == user_id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Screening)
        .where(Screening.user_id == user_id)
        .order_by(col(Screening.created_at).desc(), col(Screening.id).desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all()), count


def get_user_screening(
    *, session: Session, user_id: uuid.UUID, screening_id: uuid.UUID
) -> Screening | None:
    """One screening, only if it belongs to the user."""
    screening = session.get(Screening, screening_id)
    if screening is None or screening.user_id != user_id:
        return None
    return screening


# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user
