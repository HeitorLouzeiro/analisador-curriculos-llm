import uuid
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..docs.analise_docs import (ANALISE_DESCRIPTION, ANALISE_RESPONSES,
                                 ANALISE_SUMMARY)
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


router = APIRouter(tags=["análise"])

# Singleton do serviço de análise


def get_analise_service():
    return AnaliseService()


@router.post(
    "/analisar",
    summary=ANALISE_SUMMARY,
    description=ANALISE_DESCRIPTION,
    response_model=Dict,
    responses=ANALISE_RESPONSES
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
