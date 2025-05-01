from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.database import inicializar_db
# Importando routers
from .routers import analise_router

# Criação da aplicação FastAPI
app = FastAPI(
    title="Fabio LLM OCR API",
    description="API para análise de currículos usando OCR e LLM",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do banco de dados
inicializar_db()

# Inclusão das rotas
app.include_router(analise_router.router, prefix="/api")

# Rota de status


@app.get("/", tags=["status"])
async def status():
    """Retorna o status da API"""
    return {"status": "online", "api": "Fabio LLM OCR API"}
