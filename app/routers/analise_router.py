import uuid
from typing import Dict, List, Optional

from fastapi import (APIRouter, Body, Depends, File, Form, HTTPException,
                     UploadFile)
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..services.analise_service import AnaliseService
from ..utils.json_encoder import serializar_para_json


# Definição de modelos para exemplos da documentação
class AnaliseResultadoExemplo(BaseModel):
    arquivo: str
    resposta: Optional[str] = None
    resumo: Optional[str] = None


class AnaliseResponseExemplo(BaseModel):
    id: str = Field(example="6462a8e94f6d7b2e30a1c2d3")
    request_id: str = Field(example="e1f2a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b")
    user_id: str = Field(example="user123")
    timestamp: str = Field(example="2025-05-01T14:30:45.123Z")
    query: Optional[str] = None
    resultado: List[AnaliseResultadoExemplo]


# Exemplos para documentação
EXEMPLO_QUERY = "Desenvolvedor Python com experiência em FastAPI, MongoDB e pelo menos 2 anos de experiência"

EXEMPLO_RESPOSTA_COM_QUERY = {
    "id": "6462a8e94f6d7b2e30a1c2d3",
    "request_id": "e1f2a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b",
    "user_id": "user123",
    "timestamp": "2025-05-01T14:30:45.123Z",
    "query": EXEMPLO_QUERY,
    "resultado": [
        {
            "arquivo": "curriculo_candidato1.pdf",
            "resposta": """O currículo atende parcialmente aos requisitos da vaga.

O candidato possui sólida experiência com Python (3 anos) e conhecimento em FastAPI como mencionado no projeto de API RESTful que desenvolveu.

No entanto, não há menção explícita de experiência com MongoDB, apenas com bancos SQL.

O tempo total de experiência como desenvolvedor ultrapassa os 2 anos exigidos, com 3 anos em desenvolvimento Python.

Recomendação: Candidato potencialmente adequado, mas recomenda-se verificar durante a entrevista o conhecimento em MongoDB."""
        }
    ]
}

EXEMPLO_RESPOSTA_SEM_QUERY = {
    "id": "7563b9f95e7c8d3f41b2d3e4",
    "request_id": "f6e5d4c3-b2a1-9e8d-7f6e-5d4c3b2a1e9f",
    "user_id": "user123",
    "timestamp": "2025-05-01T15:45:30.987Z",
    "query": None,
    "resultado": [
        {
            "arquivo": "curriculo_candidato1.pdf",
            "resumo": """Nome: João Silva

Experiência:
- Desenvolvedor Backend Python (2022-atual): Implementação de APIs RESTful com FastAPI, dockerização de aplicações, testes automatizados
- Analista de Sistemas (2020-2022): Desenvolvimento de aplicações web com Django, manutenção de bancos de dados PostgreSQL

Habilidades:
- Linguagens: Python (avançado), JavaScript (intermediário), SQL (avançado)
- Frameworks: FastAPI, Django, Flask
- Ferramentas: Docker, Git, Jenkins, AWS
- Idiomas: Português (nativo), Inglês (avançado)"""
        }
    ]
}

router = APIRouter(tags=["análise"])

# Singleton do serviço de análise


def get_analise_service():
    return AnaliseService()


@router.post(
    "/analisar",
    summary="Analisa currículos",
    description="""
    Extrai texto de currículos usando OCR e realiza análise com LLM.
    
    ## Modos de operação
    
    1. **Modo Análise (com query)**: Avalia o currículo com base nos requisitos da vaga fornecidos no parâmetro `query`
    2. **Modo Resumo (sem query)**: Gera um resumo estruturado do currículo extraindo informações chave
    
    ## Parâmetros obrigatórios
    
    * **arquivos**: Um ou mais arquivos de currículo (PDF ou imagens)
    * **user_id**: Identificador do usuário que está realizando a análise
    
    ## Parâmetros opcionais
    
    * **query**: Requisitos da vaga para comparação (se omitido, gera resumo)
    * **request_id**: Identificador customizado para rastreamento da solicitação
    
    ## Formatos de arquivo aceitos
    
    PDF (.pdf) e imagens (.png, .jpg, .jpeg, .bmp, .tiff, .tif)
    """,
    response_model=Dict,
    responses={
        200: {
            "description": "Análise realizada com sucesso",
            "content": {
                "application/json": {
                    "examples": {
                        "com_query": {
                            "summary": "Exemplo de resposta com query (análise)",
                            "description": "Resposta quando uma query com requisitos é fornecida",
                            "value": EXEMPLO_RESPOSTA_COM_QUERY
                        },
                        "sem_query": {
                            "summary": "Exemplo de resposta sem query (resumo)",
                            "description": "Resposta quando nenhuma query é fornecida (resumo automático)",
                            "value": EXEMPLO_RESPOSTA_SEM_QUERY
                        }
                    }
                }
            }
        },
        415: {
            "description": "Formato de arquivo não suportado"
        },
        422: {
            "description": "Erro de validação (arquivos inválidos ou parâmetros incorretos)"
        },
        500: {
            "description": "Erro interno no processamento"
        }
    }
)
async def analisar_curriculos(
    arquivos: List[UploadFile] = File(None,
                                      description="Arquivos de currículo (PDF ou imagens)"),
    query: Optional[str] = Form(
        None, description="Requisitos da vaga para análise comparativa, se omitido gera resumo"),
    request_id: Optional[str] = Form(
        None, description="ID opcional para rastreamento da solicitação"),
    user_id: str = Form(...,
                        description="ID do usuário que está realizando a análise"),
    analise_service: AnaliseService = Depends(get_analise_service)
):
    """
    Analisa currículos usando OCR e LLM.

    - Se uma consulta for fornecida, avalia o currículo com base nos requisitos.
    - Caso contrário, resume o currículo destacando pontos principais.
    """
    try:
        # Validação personalizada para o campo arquivos
        if not arquivos or len(arquivos) == 0:
            raise HTTPException(
                status_code=422,
                detail="É necessário enviar pelo menos um arquivo de currículo para análise. Que seja PDF ou imagem."
            )

        # Garante que request_id nunca está vazio ou nulo
        if request_id is None or request_id.strip() == "":
            request_id = str(uuid.uuid4())

        resultado = await analise_service.analisar_curriculos(
            arquivos=arquivos,
            user_id=user_id,
            request_id=request_id,
            query=query
        )

        # Serializa o resultado para garantir compatibilidade JSON
        return JSONResponse(content=serializar_para_json(resultado))

    except HTTPException as http_exc:
        # Preserva o status code original da HTTPException
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar solicitação: {str(e)}")
