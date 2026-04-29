from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Schema returned after successful authentication."""

    access_token: str = Field(
        ...,
        description="Signed JWT token to be used in the Authorization header",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(
        "bearer",
        description="Token type — always 'bearer'",
        example="bearer"
    )

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenRequest(BaseModel):
    """Schema for requesting a JWT token."""

    conta_id: int = Field(
        ...,
        description="ID of the account to authenticate",
        example=1
    )

    class Config:
        schema_extra = {
            "example": {
                "conta_id": 1
            }
        }