from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoTransacao(str, Enum):
    """Enum representing the allowed transaction types."""

    DEPOSITO = "deposito"
    SAQUE = "saque"


class Transacao(Base):
    """ORM model representing a financial transaction linked to an account."""

    __tablename__ = "transacoes"

    # Primary key — auto-incremented transaction ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # Foreign key referencing the parent account — cannot be null or orphaned
    conta_id: Mapped[int] = mapped_column(
        ForeignKey("contas.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # Transaction type: deposit or withdrawal
    tipo: Mapped[str] = mapped_column(String(10), nullable=False)
    # Transaction amount — must be at least R$ 100.00
    valor: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    # Optional description provided by the user
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Timestamp when the transaction was processed
    realizada_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Many-to-one relationship: each transaction belongs to one account
    conta = relationship("Conta", back_populates="transacoes")