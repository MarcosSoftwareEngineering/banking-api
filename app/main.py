from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.database import create_tables
from app.routers import auth, contas, transacoes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await create_tables()
    yield


app = FastAPI(
    title="Banking API",
    description=(
        "API bancária de alta performance para gestão de contas e transações.\n\n"
        "## Autenticação\n"
        "Use `POST /auth/token` para obter um JWT e clique em **Authorize**.\n\n"
        "## Regras\n"
        "- Valor mínimo por transação: **R$ 100,00**\n"
        "- Saque só permitido com saldo suficiente"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(contas.router)
app.include_router(transacoes.router)


@app.exception_handler(Exception)
async def handler_generico(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno no servidor"},
    )