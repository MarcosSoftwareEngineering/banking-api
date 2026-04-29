from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transacao import Transacao


class TransacaoRepository:
    """Handles all async database operations related to transactions."""

    def __init__(self, db: AsyncSession) -> None:
        # Inject async database session
        self.db = db

    async def criar(self, conta_id: int, tipo: str, valor, descricao: str | None) -> Transacao:
        """Create and persist a new transaction record."""
        transacao = Transacao(
            conta_id=conta_id,
            tipo=tipo,
            valor=valor,
            descricao=descricao
        )
        self.db.add(transacao)
        await self.db.commit()
        await self.db.refresh(transacao)
        return transacao

    async def listar_por_conta(self, conta_id: int) -> list:
        """Return all transactions for a given account, ordered by most recent first."""
        result = await self.db.execute(
            select(Transacao)
            .where(Transacao.conta_id == conta_id)
            .order_by(Transacao.realizada_em.desc())
        )
        return list(result.scalars().all())