# 🏦 Banking API

> API bancária assíncrona de alta performance construída com FastAPI, SQLAlchemy e JWT.

---

## 🚀 Tecnologias

- **Python 3.13**
- **FastAPI** — framework web assíncrono
- **SQLAlchemy (async)** — ORM assíncrono
- **SQLite** — banco de dados
- **JWT (python-jose)** — autenticação
- **Pydantic** — validação de dados
- **Uvicorn** — servidor ASGI

---

## 📋 Funcionalidades

- ✅ Criação e listagem de contas bancárias
- ✅ Autenticação via JWT
- ✅ Depósitos e saques com validações de negócio
- ✅ Histórico de transações por conta
- ✅ Documentação interativa automática (Swagger UI)

---

## 📁 Estrutura do Projeto

```
banking-api/
├── app/
│   ├── core/          # Configurações, banco de dados e segurança
│   ├── models/        # Modelos do banco de dados
│   ├── repositories/  # Camada de acesso ao banco
│   ├── services/      # Regras de negócio
│   ├── routers/       # Endpoints da API
│   ├── schemas/       # Validação com Pydantic
│   └── exceptions/    # Exceções customizadas
├── .env
├── requirements.txt
└── main.py
```


## ⚙️ Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/MarcosSoftwareEngineering/banking-api.git
cd banking-api
```

**2. Crie o ambiente virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure o `.env`**
```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite+aiosqlite:///./banking.db
```

**5. Rode o servidor**
```bash
uvicorn app.main:app --reload
```

**6. Acesse a documentação**

http://localhost:8000/docs

---

## 🔐 Autenticação

1. Crie uma conta via `POST /contas`
2. Gere um token via `POST /auth/token`
3. Clique em **Authorize** no Swagger e cole o token

---

## 📌 Endpoints

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/contas` | Criar conta | ❌ |
| GET | `/contas` | Listar contas | ❌ |
| POST | `/auth/token` | Gerar token JWT | ❌ |
| POST | `/transacoes` | Criar transação | ✅ |
| GET | `/transacoes/{conta_id}` | Listar transações | ✅ |

---

## 👨‍💻 Autor
