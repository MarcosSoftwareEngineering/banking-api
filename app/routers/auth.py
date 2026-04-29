from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import criar_token
from app.repositories.conta_repository import ContaRepository
from app.schemas.auth import TokenRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Generate access token",
    description=(
        "Authenticates a bank account and returns a signed **JWT token**.\n\n"
        "Use the returned token in the `Authorization: Bearer <token>` header "
        "to access protected endpoints such as transactions and account statements.\n\n"
        "**Steps:**\n"
        "1. Call this endpoint with a valid `conta_id`\n"
        "2. Copy the `access_token` from the response\n"
        "3. Click **Authorize** at the top of this page and paste the token"
    ),
    responses={
        200: {
            "description": "JWT token successfully generated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        404: {
            "description": "Account not found or inactive",
            "content": {
                "application/json": {
                    "example": {"detail": "Conta não encontrada ou inativa"}
                }
            }
        }
    }
)
async def gerar_token(
    payload: TokenRequest,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    """
    Authenticate an account and return a signed JWT token.
    Raises 404 if the account does not exist or is inactive.
    """
    repo = ContaRepository(db)

    # Verify the account exists and is active before issuing a token
    conta = await repo.buscar_por_id(payload.conta_id)
    if not conta or not conta.ativa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada ou inativa"
        )

    # Encode account ID and holder name into the token payload
    token = criar_token({"sub": str(conta.id), "titular": conta.titular})
    return TokenResponse(access_token=token)