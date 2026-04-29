from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ContaNaoEncontradaError, SaldoInsuficienteError
from app.repositories.conta_repository import ContaRepository
from app.repositories.transacao_repository import TransacaoRepository
from app.schemas.transacao import TransacaoCreate


class TransacaoService:
    """Business logic layer for financial transaction operations."""

    def __init__(self, db: AsyncSession) -> None:
        # Initialize both repositories with the injected async session
        self.conta_repo = ContaRepository(db)
        self.transacao_repo = TransacaoRepository(db)

    async def processar(self, dados: TransacaoCreate):
        """
        Process a deposit or withdrawal transaction.
        Raises ContaNaoEncontradaError if account does not exist or is inactive.
        Raises SaldoInsuficienteError if withdrawal exceeds current balance.
        """
        # Validate that the target account exists and is active
        conta = await self.conta_repo.buscar_por_id(dados.conta_id)
        if not conta or not conta.ativa:
            raise ContaNaoEncontradaError(
                f"Conta {dados.conta_id} não encontrada ou inativa"
            )

        # Apply business rules based on transaction type
        if dados.tipo == "saque":
            # Ensure sufficient balance before processing withdrawal
            if conta.saldo < dados.valor:
                raise SaldoInsuficienteError(conta.saldo)
            novo_saldo = conta.saldo - dados.valor
        else:
            # Deposit: add value to current balance
            novo_saldo = conta.saldo + dados.valor

        # Persist updated balance and create transaction record
        await self.conta_repo.atualizar_saldo(conta, novo_saldo)
        return await self.transacao_repo.criar(
            conta_id=conta.id,
            tipo=dados.tipo,
            valor=dados.valor,
            descricao=dados.descricao,
        )

    async def extrato(self, conta_id: int) -> list:
        """
        Retrieve full transaction history for an account.
        Raises ContaNaoEncontradaError if account does not exist.
        """
        conta = await self.conta_repo.buscar_por_id(conta_id)
        if not conta:
            raise ContaNaoEncontradaError(f"Conta {conta_id} não encontrada")
        return await self.transacao_repo.listar_por_conta(conta_id)