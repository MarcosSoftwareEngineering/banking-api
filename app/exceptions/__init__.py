class ContaNaoEncontradaError(Exception):
    """Raised when the requested account does not exist or is inactive."""
    pass


class CPFJaCadastradoError(Exception):
    """Raised when a CPF is already registered in the system."""
    pass


class SaldoInsuficienteError(Exception):
    """Raised when an account does not have enough balance for a withdrawal."""

    def __init__(self, saldo_atual):
        self.saldo_atual = saldo_atual
        super().__init__(f"Saldo insuficiente. Saldo atual: R$ {saldo_atual:.2f}")