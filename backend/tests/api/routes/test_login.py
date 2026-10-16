from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlmodel import Session, func, select

from app import crud
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.crud import create_user
from app.models import User, UserCreate
from app.utils import generate_password_reset_token
from tests.utils.user import user_authentication_headers
from tests.utils.utils import random_email, random_lower_string


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400


def test_use_access_token(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_recovery_password(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    email = "test@example.com"
    with patch("app.api.routes.login.send_email") as mock_send_email:
        r = client.post(
            f"{settings.API_V1_STR}/password-recovery/{email}",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        assert r.json() == {
            "message": "If that email is registered, we sent a password recovery link"
        }
        mock_send_email.assert_called_once()


def test_recovery_password_user_not_exits(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    email = "jVgQr@example.com"
    r = client.post(
        f"{settings.API_V1_STR}/password-recovery/{email}",
        headers=normal_user_token_headers,
    )
    # Should return 200 with generic message to prevent email enumeration attacks
    assert r.status_code == 200
    assert r.json() == {
        "message": "If that email is registered, we sent a password recovery link"
    }


def test_reset_password(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    new_password = random_lower_string()

    user_create = UserCreate(
        email=email,
        full_name="Test User",
        password=password,
        is_active=True,
        is_superuser=False,
    )
    user = create_user(session=db, user_create=user_create)
    token = generate_password_reset_token(email=email)
    headers = user_authentication_headers(client=client, email=email, password=password)
    data = {"new_password": new_password, "token": token}

    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        headers=headers,
        json=data,
    )

    assert r.status_code == 200
    assert r.json() == {"message": "Password updated successfully"}

    db.refresh(user)
    verified, _ = verify_password(new_password, user.hashed_password)
    assert verified


def test_reset_password_invalid_token(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"new_password": "changethis", "token": "invalid"}
    r = client.post(
        f"{settings.API_V1_STR}/reset-password/",
        headers=superuser_token_headers,
        json=data,
    )
    response = r.json()

    assert "detail" in response
    assert r.status_code == 400
    assert response["detail"] == "Invalid token"


def test_login_with_bcrypt_password_upgrades_to_argon2(
    client: TestClient, db: Session
) -> None:
    """Test that logging in with a bcrypt password hash upgrades it to argon2."""
    email = random_email()
    password = random_lower_string()

    # Create a bcrypt hash directly (simulating legacy password)
    bcrypt_hasher = BcryptHasher()
    bcrypt_hash = bcrypt_hasher.hash(password)
    assert bcrypt_hash.startswith("$2")  # bcrypt hashes start with $2

    user = User(email=email, hashed_password=bcrypt_hash, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.hashed_password.startswith("$2")

    login_data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens

    db.refresh(user)

    # Verify the hash was upgraded to argon2
    assert user.hashed_password.startswith("$argon2")

    verified, updated_hash = verify_password(password, user.hashed_password)
    assert verified
    # Should not need another update since it's already argon2
    assert updated_hash is None


def test_login_with_argon2_password_keeps_hash(client: TestClient, db: Session) -> None:
    """Test that logging in with an argon2 password hash does not update it."""
    email = random_email()
    password = random_lower_string()

    # Create an argon2 hash (current default)
    argon2_hash = get_password_hash(password)
    assert argon2_hash.startswith("$argon2")

    # Create user with argon2 hash
    user = User(email=email, hashed_password=argon2_hash, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    original_hash = user.hashed_password

    login_data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens

    db.refresh(user)

    assert user.hashed_password == original_hash
    assert user.hashed_password.startswith("$argon2")


GOOGLE_URL = f"{settings.API_V1_STR}/login/google"
VERIFY = "app.api.routes.login.google_id_token.verify_oauth2_token"


def google_claims(email: str, **extra: Any) -> dict[str, Any]:
    return {
        "iss": "https://accounts.google.com",
        "aud": "test-client-id.apps.googleusercontent.com",
        "sub": random_lower_string(),
        "email": email,
        "email_verified": True,
        "name": "Siti Google",
        **extra,
    }


@pytest.fixture
def google_client_id() -> Iterator[str]:
    client_id = "test-client-id.apps.googleusercontent.com"
    with patch.object(settings, "GOOGLE_CLIENT_ID", client_id):
        yield client_id


def test_login_google_creates_user(
    client: TestClient, db: Session, google_client_id: str
) -> None:
    email = random_email()
    with patch(VERIFY, return_value=google_claims(email)) as verify:
        r = client.post(GOOGLE_URL, json={"credential": "google-id-token"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
    args = verify.call_args.args
    assert args[0] == "google-id-token"
    assert args[2] == google_client_id

    user = crud.get_user_by_email(session=db, email=email)
    assert user is not None
    assert user.is_active
    assert not user.is_superuser
    assert user.full_name == "Siti Google"
    # The random password is hashed and is not the Google token.
    assert user.hashed_password.startswith("$argon2")
    assert not verify_password("google-id-token", user.hashed_password)[0]

    me = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == email


@pytest.mark.usefixtures("google_client_id")
def test_login_google_reuses_existing_user(client: TestClient, db: Session) -> None:
    email = random_email()
    with patch(VERIFY, return_value=google_claims(email)):
        first = client.post(GOOGLE_URL, json={"credential": "token-1"})
        second = client.post(GOOGLE_URL, json={"credential": "token-2"})
    assert first.status_code == 200
    assert second.status_code == 200

    count = db.exec(
        select(func.count()).select_from(User).where(User.email == email)
    ).one()
    assert count == 1
    ids = []
    for r in (first, second):
        me = client.post(
            f"{settings.API_V1_STR}/login/test-token",
            headers={"Authorization": f"Bearer {r.json()['access_token']}"},
        )
        ids.append(me.json()["id"])
    assert ids[0] == ids[1]


@pytest.mark.usefixtures("google_client_id")
def test_login_google_links_password_account(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = create_user(
        session=db, user_create=UserCreate(email=email, password=password)
    )
    claims = google_claims(email)
    with patch(VERIFY, return_value=claims):
        first = client.post(GOOGLE_URL, json={"credential": "google-id-token"})
        second = client.post(GOOGLE_URL, json={"credential": "google-id-token-2"})
    assert first.status_code == 200
    assert second.status_code == 200
    db.refresh(user)
    # Linked on first Google sign-in; the pre-set password no longer works, so a
    # pre-registered account cannot be used to read the real owner's data.
    assert user.google_sub == claims["sub"]
    assert not verify_password(password, user.hashed_password)[0]
    old = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={"username": email, "password": password},
    )
    assert old.status_code == 400
    # The second Google sign-in reuses the same user.
    ids = []
    for r in (first, second):
        me = client.post(
            f"{settings.API_V1_STR}/login/test-token",
            headers={"Authorization": f"Bearer {r.json()['access_token']}"},
        )
        ids.append(me.json()["id"])
    assert ids[0] == ids[1] == str(user.id)


@pytest.mark.usefixtures("google_client_id")
def test_login_google_other_sub_for_linked_email_rejected(client: TestClient) -> None:
    email = random_email()
    with patch(VERIFY, return_value=google_claims(email)):
        assert client.post(GOOGLE_URL, json={"credential": "a"}).status_code == 200
    with patch(VERIFY, return_value=google_claims(email)):
        r = client.post(GOOGLE_URL, json={"credential": "b"})
    assert r.status_code == 400


@pytest.mark.usefixtures("google_client_id")
def test_login_google_unverified_email_rejected(
    client: TestClient, db: Session
) -> None:
    email = random_email()
    claims = google_claims(email, email_verified=False)
    with patch(VERIFY, return_value=claims):
        r = client.post(GOOGLE_URL, json={"credential": "google-id-token"})
    assert r.status_code == 400
    assert crud.get_user_by_email(session=db, email=email) is None


@pytest.mark.usefixtures("google_client_id")
def test_login_google_invalid_token(client: TestClient) -> None:
    with patch(VERIFY, side_effect=ValueError("Token expired")):
        r = client.post(GOOGLE_URL, json={"credential": "bad-token"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid Google credential"


@pytest.mark.usefixtures("google_client_id")
def test_login_google_inactive_user(client: TestClient, db: Session) -> None:
    email = random_email()
    user = User(
        email=email, hashed_password=get_password_hash("x" * 12), is_active=False
    )
    db.add(user)
    db.commit()
    with patch(VERIFY, return_value=google_claims(email)):
        r = client.post(GOOGLE_URL, json={"credential": "google-id-token"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Inactive user"


def test_login_google_not_configured(client: TestClient) -> None:
    verify = MagicMock()
    with (
        patch.object(settings, "GOOGLE_CLIENT_ID", None),
        patch(VERIFY, verify),
    ):
        r = client.post(GOOGLE_URL, json={"credential": "google-id-token"})
    assert r.status_code == 503
    verify.assert_not_called()
