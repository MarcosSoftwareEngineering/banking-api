from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings


def criar_token(data: dict) -> str:
    """Create a signed JWT token with expiration time."""
    payload = data.copy()
    # Set token expiration based on configured minutes
    expira = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decodificar_token(token: str) -> dict:
    """Decode and validate a JWT token. Returns empty dict if invalid."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return {}