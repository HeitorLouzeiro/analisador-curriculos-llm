from typing import Dict, List, Optional

from fastapi import HTTPException, UploadFile

from ..models.log import AnaliseResultado, LogAnalise
from ..repositories.log_repository import LogRepository
from ..services.llm_service import LLMService, ModelNotFoundException
from ..services.ocr_service import OCRService


class AnaliseService:
    def __init__(self):
        self.ocr_service = OCRService()
        self.llm_service = LLMService()
        self.log_repository = LogRepository()

    async def processar_curriculo(self, texto: str, filename: str, query: Optional[str] = None) -> Dict:
        """Processa um único currículo e retorna o resultado."""
        try:
            if query:
                # Análise com requisitos específicos
                prompt = self.llm_service.criar_prompt_analise(texto, query)
                resposta = self.llm_service.consultar_llm(prompt)
                return {"arquivo": filename, "resposta": resposta}
            else:
                # Resumo do currículo
                prompt = self.llm_service.criar_prompt_resumo(texto)
                resumo = self.llm_service.consultar_llm(prompt)
                return {"arquivo": filename, "resumo": resumo}
        except ModelNotFoundException as e:
            # Propagando a exceção específica para ser tratada no nível do router
            raise HTTPException(
                status_code=503,
                detail=f"Serviço de LLM indisponível: {str(e)}"
            )
        except Exception as e:
            print(f"Erro ao processar currículo {filename}: {e}")
            return {"arquivo": filename, "erro": str(e)}

    async def analisar_curriculos(
        self,
        arquivos: List[UploadFile],
        user_id: str,
        request_id: Optional[str] = None,
        query: Optional[str] = None
    ) -> Dict:
        """Analisa uma lista de currículos e retorna o resultado."""
        # Extrai texto dos arquivos
        textos = await self.ocr_service.extrair_texto_arquivos(arquivos)

        # Processa cada currículo
        resultados = []
        for i, texto in enumerate(textos):
            resultado = await self.processar_curriculo(texto, arquivos[i].filename, query)
            resultados.append(resultado)

        # Cria e salva o log da análise
        resultados_modelos = [AnaliseResultado(
            **resultado) for resultado in resultados]

        # Cria o log com todos os parâmetros incluindo request_id
        # O request_id já foi garantido como não nulo na camada do router
        log_params = {
            "user_id": user_id,
            "query": query,
            "request_id": request_id,
            "resultado": resultados_modelos
        }

        log = LogAnalise(**log_params)

        # Salva no repositório
        return self.log_repository.inserir_log(log)
