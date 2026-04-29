from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Conta(Base):
    """ORM model representing a bank account (conta corrente)."""

    __tablename__ = "contas"

    # Primary key — auto-incremented account ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Full name of the account holder
    titular: Mapped[str] = mapped_column(String(100), nullable=False)
    # Brazilian tax ID (CPF) — must be unique across all accounts
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False, index=True)
    # Current account balance — defaults to zero
    saldo: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"))
    # Soft-delete flag — inactive accounts cannot perform transactions
    ativa: Mapped[bool] = mapped_column(default=True)
    # Timestamp of account creation
    criada_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # One-to-many relationship: one account has many transactions
    transacoes = relationship(
        "Transacao", back_populates="conta", cascade="all, delete-orphan"
    )