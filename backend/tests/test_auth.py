"""
Authentication endpoint and service tests.

Tests for registration, login, JWT token handling, password hashing,
and protected endpoint access.

Uses mocked database fixtures — no live PostgreSQL required.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone, timedelta

from app.services.auth import hash_password, verify_password, create_access_token, decode_access_token


# ═══════════════════════════════════════════════════════════════
# Password Hashing Tests
# ═══════════════════════════════════════════════════════════════

class TestPasswordHashing:
    """Test bcrypt password hashing and verification."""

    def test_hash_password_returns_hash(self):
        """hash_password should return a bcrypt hash string."""
        hashed = hash_password("MySecure123!")
        assert hashed is not None
        assert hashed != "MySecure123!"
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """verify_password should return True for correct password."""
        hashed = hash_password("MySecure123!")
        assert verify_password("MySecure123!", hashed) is True

    def test_verify_password_wrong(self):
        """verify_password should return False for wrong password."""
        hashed = hash_password("MySecure123!")
        assert verify_password("WrongPassword!", hashed) is False

    def test_hash_is_unique_per_call(self):
        """Each hash should use a unique salt."""
        h1 = hash_password("SamePassword")
        h2 = hash_password("SamePassword")
        assert h1 != h2  # Different salts


# ═══════════════════════════════════════════════════════════════
# JWT Token Tests
# ═══════════════════════════════════════════════════════════════

class TestJWTTokens:
    """Test JWT token creation and validation."""

    def test_create_access_token(self):
        """create_access_token should return a non-empty string."""
        token = create_access_token(subject="42")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_valid_token(self):
        """decode_access_token should return the payload for a valid token."""
        token = create_access_token(subject="42")
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "42"

    def test_decode_expired_token(self):
        """decode_access_token should return None for an expired token."""
        token = create_access_token(
            subject="42",
            expires_delta=timedelta(seconds=-1),
        )
        payload = decode_access_token(token)
        assert payload is None

    def test_decode_invalid_token(self):
        """decode_access_token should return None for a garbage token."""
        payload = decode_access_token("not.a.valid.token")
        assert payload is None

    def test_token_contains_iat(self):
        """Token payload should contain an 'iat' (issued at) claim."""
        token = create_access_token(subject="42")
        payload = decode_access_token(token)
        assert "iat" in payload

    def test_token_contains_exp(self):
        """Token payload should contain an 'exp' (expiration) claim."""
        token = create_access_token(subject="42")
        payload = decode_access_token(token)
        assert "exp" in payload


# ═══════════════════════════════════════════════════════════════
# Registration Endpoint Tests
# ═══════════════════════════════════════════════════════════════

class TestRegistration:
    """Test POST /api/v1/auth/register."""

    @pytest.mark.asyncio
    async def test_register_success(self, client):
        """Successful registration should return 201 with user profile."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.display_name = "Test User"
        mock_user.is_active = True
        mock_user.created_at = datetime.now(timezone.utc)
        mock_user.last_login_at = None

        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=None), \
             patch("app.api.v1.auth.create_user", new_callable=AsyncMock, return_value=mock_user):

            response = await client.post("/api/v1/auth/register", json={
                "email": "test@example.com",
                "password": "SecurePass123!",
                "display_name": "Test User",
            })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["display_name"] == "Test User"
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client):
        """Registration with existing email should return 409."""
        existing_user = MagicMock()
        existing_user.email = "test@example.com"

        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=existing_user):
            response = await client.post("/api/v1/auth/register", json={
                "email": "test@example.com",
                "password": "SecurePass123!",
                "display_name": "Test User",
            })

        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_short_password(self, client):
        """Registration with password < 8 chars should return 422."""
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "short",
            "display_name": "Test User",
        })
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client):
        """Registration with invalid email should return 422."""
        response = await client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "SecurePass123!",
            "display_name": "Test User",
        })
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_display_name(self, client):
        """Registration without display_name should return 422."""
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "SecurePass123!",
        })
        assert response.status_code == 422


# ═══════════════════════════════════════════════════════════════
# Login Endpoint Tests
# ═══════════════════════════════════════════════════════════════

class TestLogin:
    """Test POST /api/v1/auth/login."""

    @pytest.mark.asyncio
    async def test_login_success(self, client):
        """Successful login should return JWT token."""
        hashed = hash_password("SecurePass123!")
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.hashed_password = hashed
        mock_user.is_active = True

        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=mock_user), \
             patch("app.api.v1.auth.update_last_login", new_callable=AsyncMock):

            response = await client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "SecurePass123!",
            })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client):
        """Login with wrong password should return 401."""
        hashed = hash_password("CorrectPassword!")
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.hashed_password = hashed
        mock_user.is_active = True

        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=mock_user):
            response = await client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "WrongPassword!",
            })

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """Login with non-existent email should return 401."""
        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=None):
            response = await client.post("/api/v1/auth/login", json={
                "email": "nobody@example.com",
                "password": "SomePassword!",
            })

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_deactivated_user(self, client):
        """Login with deactivated account should return 403."""
        hashed = hash_password("SecurePass123!")
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.hashed_password = hashed
        mock_user.is_active = False

        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=mock_user):
            response = await client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "SecurePass123!",
            })

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_login_returns_valid_jwt(self, client):
        """The returned token should be a valid, decodable JWT."""
        hashed = hash_password("SecurePass123!")
        mock_user = MagicMock()
        mock_user.id = 42
        mock_user.email = "test@example.com"
        mock_user.hashed_password = hashed
        mock_user.is_active = True

        with patch("app.api.v1.auth.get_user_by_email", new_callable=AsyncMock, return_value=mock_user), \
             patch("app.api.v1.auth.update_last_login", new_callable=AsyncMock):

            response = await client.post("/api/v1/auth/login", json={
                "email": "test@example.com",
                "password": "SecurePass123!",
            })

        token = response.json()["access_token"]
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "42"


# ═══════════════════════════════════════════════════════════════
# Protected Endpoint Tests (/me)
# ═══════════════════════════════════════════════════════════════

class TestProtectedEndpoint:
    """Test GET /api/v1/auth/me (requires authentication)."""

    @pytest.mark.asyncio
    async def test_me_with_valid_token(self, client):
        """Authenticated request should return user profile."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.display_name = "Test User"
        mock_user.is_active = True
        mock_user.is_superuser = False
        mock_user.created_at = datetime.now(timezone.utc)
        mock_user.last_login_at = None

        token = create_access_token(subject="1")

        with patch("app.api.deps.get_user_by_id", new_callable=AsyncMock, return_value=mock_user):
            response = await client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["display_name"] == "Test User"

    @pytest.mark.asyncio
    async def test_me_without_token(self, client):
        """Request without token should return 401."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_with_invalid_token(self, client):
        """Request with garbage token should return 401."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer garbage.token.here"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_with_expired_token(self, client):
        """Request with expired token should return 401."""
        token = create_access_token(
            subject="1",
            expires_delta=timedelta(seconds=-1),
        )
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_with_deleted_user(self, client):
        """Token for a non-existent user should return 401."""
        token = create_access_token(subject="999")

        with patch("app.api.deps.get_user_by_id", new_callable=AsyncMock, return_value=None):
            response = await client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_with_deactivated_user(self, client):
        """Token for a deactivated user should return 403."""
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.is_active = False

        token = create_access_token(subject="1")

        with patch("app.api.deps.get_user_by_id", new_callable=AsyncMock, return_value=mock_user):
            response = await client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 403
