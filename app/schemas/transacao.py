from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, validator

# Minimum allowed transaction amount as per business rules
VALOR_MINIMO = Decimal("100.00")


class TransacaoCreate(BaseModel):
    """Schema for creating a new transaction (deposit or withdrawal)."""

    conta_id: int = Field(
        ...,
        description="ID of the target bank account",
        example=1
    )
    tipo: str = Field(
        ...,
        description="Transaction type: 'deposito' for deposit, 'saque' for withdrawal",
        example="deposito"
    )
    valor: Decimal = Field(
        ...,
        description="Transaction amount in BRL — minimum value is R$ 100.00",
        example=500.00
    )
    descricao: str | None = Field(
        None,
        max_length=255,
        description="Optional description or note for the transaction",
        example="Monthly salary deposit"
    )

    @validator("tipo")
    def validar_tipo(cls, v):
        # Only 'deposito' and 'saque' are valid transaction types
        if v not in ("deposito", "saque"):
            raise ValueError("Tipo deve ser 'deposito' ou 'saque'")
        return v

    @validator("valor")
    def validar_valor(cls, v):
        # Enforce minimum transaction amount of R$ 100.00
        if v < VALOR_MINIMO:
            raise ValueError(f"Valor mínimo é R$ {VALOR_MINIMO:.2f}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "conta_id": 1,
                "tipo": "deposito",
                "valor": 500.00,
                "descricao": "Monthly salary deposit"
            }
        }


class TransacaoResponse(BaseModel):
    """Schema returned after a transaction is successfully processed."""

    id: int = Field(..., description="Unique transaction identifier", example=1)
    conta_id: int = Field(..., description="ID of the associated bank account", example=1)
    tipo: str = Field(..., description="Transaction type: deposito or saque", example="deposito")
    valor: Decimal = Field(..., description="Transaction amount in BRL", example=500.00)
    descricao: str | None = Field(None, description="Optional transaction description", example="Monthly salary deposit")
    realizada_em: datetime = Field(..., description="Timestamp when the transaction was processed")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "conta_id": 1,
                "tipo": "deposito",
                "valor": 500.00,
                "descricao": "Monthly salary deposit",
                "realizada_em": "2024-01-15T10:30:00"
            }
        }