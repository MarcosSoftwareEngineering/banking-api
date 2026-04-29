from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decodificar_token
from app.exceptions import SaldoInsuficienteError, ContaNaoEncontradaError
from app.schemas.transacao import TransacaoCreate, TransacaoResponse
from app.services.transacao_service import TransacaoService

# Router for transaction endpoints — all routes prefixed with /transacoes
router = APIRouter(prefix="/transacoes", tags=["Transações"])


@router.post(
    "",
    response_model=TransacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction",
    description=(
        "Creates a new **deposit** or **withdrawal** transaction for a bank account.\n\n"
        "**Validations:**\n"
        "- `tipo` must be `'deposito'` or `'saque'`\n"
        "- `valor` must be at least **R$ 100.00**\n"
        "- For withdrawals, the account must have sufficient balance\n"
        "- The target account must be active\n\n"
        "**Authentication required** — pass a valid JWT token in the "
        "`Authorization: Bearer <token>` header."
    ),
    responses={
        201: {
            "description": "Transaction successfully processed",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "conta_id": 1,
                        "tipo": "deposito",
                        "valor": 500.00,
                        "descricao": "Monthly salary deposit",
                        "realizada_em": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        400: {
            "description": "Insufficient balance or inactive account",
            "content": {
                "application/json": {
                    "examples": {
                        "saldo_insuficiente": {
                            "summary": "Insufficient balance",
                            "value": {"detail": "Saldo insuficiente para realizar o saque"}
                        },
                        "conta_inativa": {
                            "summary": "Inactive account",
                            "value": {"detail": "Conta inativa — operação não permitida"}
                        }
                    }
                }
            }
        },
        401: {
            "description": "Missing or invalid authentication token",
            "content": {
                "application/json": {
                    "example": {"detail": "Token inválido ou expirado"}
                }
            }
        },
        404: {
            "description": "Account not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Conta não encontrada"}
                }
            }
        },
        422: {
            "description": "Validation error — invalid tipo or valor below minimum",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "valor"],
                                "msg": "Valor mínimo é R$ 100.00",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def criar_transacao(
    dados: TransacaoCreate,
    db: AsyncSession = Depends(get_db),
    # Decode JWT token to authenticate the request
    payload: dict = Depends(decodificar_token)
) -> TransacaoResponse:
    """
    Process a deposit or withdrawal transaction.
    Raises 400 for insufficient balance or inactive account.
    Raises 404 if the account does not exist.
    """
    service = TransacaoService(db)
    try:
        # Delegate business logic to the service layer
        transacao = await service.processar(dados)
        return TransacaoResponse.from_orm(transacao)
    except SaldoInsuficienteError as e:
        # Return 400 if the account does not have enough funds
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ContaNaoEncontradaError as e:
        # Return 404 if the account does not exist or is inactive
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{conta_id}",
    response_model=list[TransacaoResponse],
    summary="List transactions by account",
    description=(
        "Returns all **transactions** associated with a specific bank account.\n\n"
        "Results are ordered by **most recent first**.\n\n"
        "**Authentication required** — pass a valid JWT token in the "
        "`Authorization: Bearer <token>` header."
    ),
    responses={
        200: {
            "description": "List of transactions returned successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 2,
                            "conta_id": 1,
                            "tipo": "saque",
                            "valor": 200.00,
                            "descricao": "ATM withdrawal",
                            "realizada_em": "2024-01-16T14:00:00"
                        },
                        {
                            "id": 1,
                            "conta_id": 1,
                            "tipo": "deposito",
                            "valor": 500.00,
                            "descricao": "Monthly salary deposit",
                            "realizada_em": "2024-01-15T10:30:00"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Account not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Conta não encontrada"}
                }
            }
        }
    }
)
async def listar_transacoes(
    conta_id: int,
    db: AsyncSession = Depends(get_db),
    # Decode JWT token to authenticate the request
    payload: dict = Depends(decodificar_token)
) -> list[TransacaoResponse]:
    """
    Retrieve all transactions for the given account ID, ordered by most recent.
    Raises 404 if the account does not exist.
    """
    service = TransacaoService(db)
    # Fetch all transactions linked to the given account
    transacoes = await service.listar_por_conta(conta_id)
    return [TransacaoResponse.from_orm(t) for t in transacoes]