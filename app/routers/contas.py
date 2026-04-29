from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.exceptions import CPFJaCadastradoError
from app.schemas.conta import ContaCreate, ContaListResponse, ContaResponse
from app.services.conta_service import ContaService

router = APIRouter(prefix="/contas", tags=["Contas"])


@router.post(
    "",
    response_model=ContaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create bank account",
    description=(
        "Creates a new **bank account** in the system.\n\n"
        "**Validations:**\n"
        "- `titular` must be between 3 and 100 characters\n"
        "- `cpf` must contain exactly 11 numeric digits\n"
        "- CPF must be unique — duplicate CPFs are rejected with 409\n\n"
        "The account is created with a **zero balance** and is immediately active."
    ),
    responses={
        201: {
            "description": "Account successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "titular": "João da Silva",
                        "cpf": "12345678900",
                        "saldo": 0.00,
                        "ativa": True,
                        "criada_em": "2024-01-15T10:30:00"
                    }
                }
            }
        },
        409: {
            "description": "CPF already registered",
            "content": {
                "application/json": {
                    "example": {"detail": "CPF 12345678900 já cadastrado"}
                }
            }
        },
        422: {
            "description": "Validation error — invalid CPF format or missing fields",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "cpf"],
                                "msg": "CPF deve conter exatamente 11 números",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def criar_conta(
    dados: ContaCreate,
    db: AsyncSession = Depends(get_db)
) -> ContaResponse:
    """
    Create a new bank account with the provided holder name and CPF.
    Raises 409 if the CPF is already registered.
    """
    service = ContaService(db)
    try:
        conta = await service.criar_conta(dados)
        return ContaResponse.from_orm(conta)
    except CPFJaCadastradoError as e:
        # CPF conflict — return 409 with descriptive error message
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "",
    response_model=list[ContaListResponse],
    summary="List bank accounts",
    description=(
        "Returns a list of all **active bank accounts** registered in the system.\n\n"
        "Inactive accounts are automatically excluded from the results.\n\n"
        "This endpoint is **public** and does not require authentication."
    ),
    responses={
        200: {
            "description": "List of active accounts returned successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "titular": "João da Silva",
                            "cpf": "12345678900",
                            "saldo": 1500.00,
                            "ativa": True
                        },
                        {
                            "id": 2,
                            "titular": "Maria Souza",
                            "cpf": "98765432100",
                            "saldo": 3200.00,
                            "ativa": True
                        }
                    ]
                }
            }
        }
    }
)
async def listar_contas(
    db: AsyncSession = Depends(get_db)
) -> list[ContaListResponse]:
    """Retrieve and return a list of all active bank accounts."""
    service = ContaService(db)
    contas = await service.listar_contas()
    return [ContaListResponse.from_orm(c) for c in contas]