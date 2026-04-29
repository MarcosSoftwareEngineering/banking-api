from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conta import Conta


class ContaRepository:
    """Handles all async database operations related to bank accounts."""

    def __init__(self, db: AsyncSession) -> None:
        # Inject async database session
        self.db = db

    async def criar(self, titular: str, cpf: str) -> Conta:
        """Create and persist a new bank account."""
        conta = Conta(titular=titular, cpf=cpf)
        self.db.add(conta)
        await self.db.commit()
        await self.db.refresh(conta)
        return conta

    async def listar(self) -> list:
        """Return all active bank accounts."""
        result = await self.db.execute(select(Conta).where(Conta.ativa == True))
        return list(result.scalars().all())

    async def buscar_por_id(self, conta_id: int) -> Conta | None:
        """Find a single account by its ID. Returns None if not found."""
        result = await self.db.execute(select(Conta).where(Conta.id == conta_id))
        return result.scalar_one_or_none()

    async def buscar_por_cpf(self, cpf: str) -> Conta | None:
        """Find a single account by CPF. Returns None if not found."""
        result = await self.db.execute(select(Conta).where(Conta.cpf == cpf))
        return result.scalar_one_or_none()

    async def atualizar_saldo(self, conta: Conta, novo_saldo) -> Conta:
        """Update the account balance and persist the change."""
        conta.saldo = novo_saldo
        await self.db.commit()
        await self.db.refresh(conta)
        return conta