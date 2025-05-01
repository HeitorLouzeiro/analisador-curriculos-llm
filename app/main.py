import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config.database import inicializar_db
# Importando routers
from .routers import analise_router

# Configuração dos templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Criação da aplicação FastAPI
app = FastAPI(
    title="Fabio LLM OCR API",
    description="""
    # API para análise inteligente de currículos
    
    Esta API combina Reconhecimento Óptico de Caracteres (OCR) com Modelos de Linguagem (LLM)
    para extrair e analisar informações de currículos.
    
    ## Funcionalidades
    
    * **Extração de texto** de arquivos PDF e imagens usando OCR avançado
    * **Análise de currículos** com base em requisitos específicos de vagas
    * **Resumo automático** de currículos destacando pontos principais
    
    ## Como usar
    
    1. Envie currículos através do endpoint `/api/analisar`
    2. Forneça uma _query_ com requisitos para análise comparativa ou deixe em branco para resumo automático
    3. Receba respostas estruturadas em JSON com a análise ou resumo de cada documento
    
    ## Observações técnicas
    
    * Suporta arquivos PDF e imagens (.jpg, .png, etc.)
    * Processamento assíncrono para melhor performance
    * Configuração do modelo LLM pode ser ajustada para diferentes casos de uso
    """,
    version="1.0.0",
    docs_url=None,  # Desativa o endpoint /docs padrão para personalizá-lo
    redoc_url="/redoc",  # Mantém a documentação ReDoc
    openapi_tags=[
        {"name": "análise", "description": "Operações de análise de currículos"}
    ]
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

# Endpoint personalizado para o Swagger UI


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Documentação API",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )

# Página do guia da API personalizado


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def api_guide():
    """Retorna a página de guia da API com exemplos detalhados"""
    return templates.TemplateResponse("api_guide.html", {"request": {}})
