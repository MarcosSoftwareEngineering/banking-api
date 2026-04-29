from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import CPFJaCadastradoError
from app.repositories.conta_repository import ContaRepository
from app.schemas.conta import ContaCreate


class ContaService:
    """Business logic layer for bank account operations."""

    def __init__(self, db: AsyncSession) -> None:
        # Initialize repository with the injected async session
        self.repo = ContaRepository(db)

    async def criar_conta(self, dados: ContaCreate):
        """
        Create a new bank account.
        Raises CPFJaCadastradoError if the CPF is already registered.
        """
        # Check for duplicate CPF before creating
        existente = await self.repo.buscar_por_cpf(dados.cpf)
        if existente:
            raise CPFJaCadastradoError(f"CPF {dados.cpf} já cadastrado")
        return await self.repo.criar(titular=dados.titular, cpf=dados.cpf)

    async def listar_contas(self) -> list:
        """Return all active bank accounts."""
        return await self.repo.listar()