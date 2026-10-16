import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlmodel import Session, col, delete, select

from app import crud
from app.core.config import settings
from app.models import Screening, User, UserCreate
from tests.utils.user import user_authentication_headers
from tests.utils.utils import random_email, random_lower_string

HISTORY_URL = f"{settings.API_V1_STR}/users/me/screenings"


def make_user(db: Session) -> tuple[User, str]:
    password = random_lower_string()
    user = crud.create_user(
        session=db,
        user_create=UserCreate(email=random_email(), password=password),
    )
    return user, password


def login(client: TestClient, user: User, password: str) -> dict[str, str]:
    return user_authentication_headers(
        client=client, email=user.email, password=password
    )


def add_screening(
    db: Session,
    user: User | None,
    *,
    top_disease: str | None = "dbd",
    created_at: datetime | None = None,
) -> Screening:
    screening = Screening(
        user_id=user.id if user else None,
        flow_id="infection",
        answers={"q1": ["fever"]},
        route="KUNING",
        unknown=False,
        top_disease=top_disease,
        top_score=0.72,
        engine="rules",
        created_at=created_at or datetime.now(UTC),
    )
    db.add(screening)
    db.commit()
    db.refresh(screening)
    return screening


def test_history_returns_only_own_newest_first(client: TestClient, db: Session) -> None:
    me, password = make_user(db)
    other, _ = make_user(db)
    now = datetime.now(UTC)
    older = add_screening(db, me, top_disease="tifoid", created_at=now - timedelta(1))
    newer = add_screening(db, me, top_disease="dbd", created_at=now)
    add_screening(db, other)
    add_screening(db, None)

    r = client.get(HISTORY_URL, headers=login(client, me, password))
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    assert [item["id"] for item in body["data"]] == [str(newer.id), str(older.id)]
    item = body["data"][0]
    assert set(item) == {
        "id",
        "flow_id",
        "route",
        "unknown",
        "top_disease",
        "top_score",
        "created_at",
    }
    assert item["top_disease"] == "dbd"
    assert item["top_score"] == 0.72
    assert item["route"] == "KUNING"


def test_history_pagination(client: TestClient, db: Session) -> None:
    me, password = make_user(db)
    now = datetime.now(UTC)
    rows = [
        add_screening(db, me, created_at=now - timedelta(minutes=i)) for i in range(3)
    ]
    headers = login(client, me, password)

    r = client.get(HISTORY_URL, headers=headers, params={"skip": 1, "limit": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 3
    assert [item["id"] for item in body["data"]] == [str(rows[1].id)]

    assert (
        client.get(HISTORY_URL, headers=headers, params={"limit": 0}).status_code == 422
    )


def test_history_requires_login(client: TestClient) -> None:
    assert client.get(HISTORY_URL).status_code == 401


def test_delete_own_screening(client: TestClient, db: Session) -> None:
    me, password = make_user(db)
    screening = add_screening(db, me)
    screening_id = screening.id

    r = client.delete(
        f"{HISTORY_URL}/{screening_id}", headers=login(client, me, password)
    )
    assert r.status_code == 200
    db.expire_all()
    assert db.get(Screening, screening_id) is None


def test_delete_someone_elses_screening_is_404(client: TestClient, db: Session) -> None:
    me, password = make_user(db)
    other, _ = make_user(db)
    theirs = add_screening(db, other)
    anonymous = add_screening(db, None)
    headers = login(client, me, password)

    for screening in (theirs, anonymous):
        r = client.delete(f"{HISTORY_URL}/{screening.id}", headers=headers)
        assert r.status_code == 404
    r = client.delete(f"{HISTORY_URL}/{uuid.uuid4()}", headers=headers)
    assert r.status_code == 404

    db.expire_all()
    assert db.get(Screening, theirs.id) is not None
    assert db.get(Screening, anonymous.id) is not None


def test_delete_me_removes_my_screenings(client: TestClient, db: Session) -> None:
    me, password = make_user(db)
    other, _ = make_user(db)
    mine = [add_screening(db, me).id for _ in range(2)]
    theirs = add_screening(db, other).id

    r = client.delete(
        f"{settings.API_V1_STR}/users/me", headers=login(client, me, password)
    )
    assert r.status_code == 200

    db.expire_all()
    left = db.exec(select(Screening).where(col(Screening.id).in_(mine))).all()
    assert left == []
    assert db.get(Screening, theirs) is not None


def test_superuser_delete_user_removes_screenings(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    user, _ = make_user(db)
    screening_id = add_screening(db, user).id

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}", headers=superuser_token_headers
    )
    assert r.status_code == 200

    db.expire_all()
    assert db.get(Screening, screening_id) is None


def test_db_cascade_without_orm(db: Session) -> None:
    """The FK itself cascades, so a bulk delete outside the ORM is safe too."""
    user, _ = make_user(db)
    screening_id = add_screening(db, user).id
    user_id = user.id
    db.expunge_all()

    db.execute(delete(User).where(col(User.id) == user_id))
    db.commit()
    assert db.get(Screening, screening_id) is None
