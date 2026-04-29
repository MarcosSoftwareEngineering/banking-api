from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, validator


class ContaCreate(BaseModel):
    """Schema for creating a new bank account."""

    titular: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Full name of the account holder",
        example="João da Silva"
    )
    cpf: str = Field(
        ...,
        min_length=11,
        max_length=11,
        description="Brazilian tax ID — exactly 11 numeric digits, no punctuation",
        example="12345678900"
    )

    @validator("cpf")
    def validar_cpf(cls, v):
        # CPF must contain exactly 11 numeric digits
        if not v.isdigit() or len(v) != 11:
            raise ValueError("CPF deve conter exatamente 11 números")
        return v

    class Config:
        schema_extra = {
            "example": {
                "titular": "João da Silva",
                "cpf": "12345678900"
            }
        }


class ContaResponse(BaseModel):
    """Full account response schema — returned after creation."""

    id: int = Field(..., description="Unique account identifier", example=1)
    titular: str = Field(..., description="Full name of the account holder", example="João da Silva")
    cpf: str = Field(..., description="Brazilian tax ID of the account holder", example="12345678900")
    saldo: Decimal = Field(..., description="Current account balance in BRL", example=1500.00)
    ativa: bool = Field(..., description="Whether the account is active", example=True)
    criada_em: datetime = Field(..., description="Timestamp when the account was created")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "titular": "João da Silva",
                "cpf": "12345678900",
                "saldo": 1500.00,
                "ativa": True,
                "criada_em": "2024-01-15T10:30:00"
            }
        }


class ContaListResponse(BaseModel):
    """Simplified account schema — used in list responses."""

    id: int = Field(..., description="Unique account identifier", example=1)
    titular: str = Field(..., description="Full name of the account holder", example="João da Silva")
    cpf: str = Field(..., description="Brazilian tax ID of the account holder", example="12345678900")
    saldo: Decimal = Field(..., description="Current account balance in BRL", example=1500.00)
    ativa: bool = Field(..., description="Whether the account is active", example=True)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "titular": "João da Silva",
                "cpf": "12345678900",
                "saldo": 1500.00,
                "ativa": True
            }
        }