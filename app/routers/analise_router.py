from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from ..services.analise_service import AnaliseService
from ..utils.json_encoder import serializar_para_json

router = APIRouter(tags=["análise"])

# Singleton do serviço de análise


def get_analise_service():
    return AnaliseService()


@router.post("/analisar", summary="Analisa currículos")
async def analisar_curriculos(
    arquivos: List[UploadFile] = File(...),
    query: Optional[str] = Form(None),
    request_id: str = Form(...),
    user_id: str = Form(...),
    analise_service: AnaliseService = Depends(get_analise_service)
):
    """
    Analisa currículos usando OCR e LLM.

    - Se uma consulta for fornecida, avalia o currículo com base nos requisitos.
    - Caso contrário, resume o currículo destacando pontos principais.
    """
    try:
        resultado = await analise_service.analisar_curriculos(
            arquivos=arquivos,
            request_id=request_id,
            user_id=user_id,
            query=query
        )

        # Serializa o resultado para garantir compatibilidade JSON
        return JSONResponse(content=serializar_para_json(resultado))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar solicitação: {str(e)}")


@router.get("/logs/{user_id}", summary="Recupera logs de análises por usuário")
async def obter_logs_por_usuario(
    user_id: str,
    analise_service: AnaliseService = Depends(get_analise_service)
):
    """
    Recupera todos os logs de análises feitas por um determinado usuário.
    """
    try:
        logs = analise_service.log_repository.buscar_logs_por_usuario(user_id)
        return JSONResponse(content=serializar_para_json(logs))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar logs: {str(e)}")
