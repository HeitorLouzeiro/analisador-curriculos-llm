import time
from typing import Dict, Optional

import requests


class LLMService:
    def __init__(self, base_url="http://ollama:11434"):
        self.base_url = base_url
        self.default_model = "llama3.2"
        self.fallback_model = "phi"

    def criar_prompt_analise(self, texto: str, query: str) -> str:
        """Cria um prompt para análise de currículo com requisitos específicos."""
        return f"""
                    Você é um especialista em RH. Avalie o currículo abaixo em relação aos requisitos:
                    "{query}"

                    Currículo:
                    {texto}

                    Responda se ele atende aos requisitos e justifique.

                    Responda a perguntas do tipo "Qual desses currículos se enquadra melhor 
                    para a vaga de Engenheiro de Software com requisitos {...}?" com 
                    justificativas baseadas no conteúdo.

                    E me responda em português. (obrigatório!)
                """

    def criar_prompt_resumo(self, texto: str) -> str:
        """Cria um prompt para resumir um currículo."""
        return f"""
                    ** Solicitação de Resumo de curriculo, sendo respondido em portugues.**

                    # Curriculo do candidato para resumir:
                    {texto}

                    **Formato de Output Esperado:**
                    - Nome: Nome do candidato

                    ** Experiência: **
                    - Experiência profissional do candidato

                    **Habilidades **
                    - Habilidades do candidato
                """

    def consultar_llm(self, prompt: str, model: Optional[str] = None) -> str:
        """Consulta o LLM usando o modelo especificado ou o padrão."""
        model = model or self.default_model

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            json_response = response.json()

            # Verifica se há erro de memória
            if "error" in json_response and "memory" in json_response["error"].lower():
                print(
                    f"Erro de memória com modelo {model}. Tentando com modelo menor...")
                return self._tentar_com_modelo_alternativo(prompt)

            # Lidando com diferentes formatos de resposta
            if "response" in json_response:
                return json_response["response"]
            elif "response_data" in json_response:
                return json_response["response_data"]
            elif "generation" in json_response:
                return json_response["generation"]
            elif "error" in json_response:
                return f"Erro do modelo: {json_response['error']}"
            else:
                print(f"Estrutura da resposta: {json_response}")
                return str(json_response)

        except Exception as e:
            print(f"Erro ao consultar LLM: {e}")
            return f"Erro: {str(e)}"

    def _tentar_com_modelo_alternativo(self, prompt: str) -> str:
        """Tenta consultar LLM usando o modelo alternativo."""
        try:
            # Baixa o modelo alternativo, se necessário
            requests.post(
                f"{self.base_url}/api/pull",
                json={"model": self.fallback_model}
            )
            time.sleep(2)  # Aguarda carregamento do modelo

            # Tenta novamente com o modelo alternativo
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.fallback_model,
                      "prompt": prompt, "stream": False}
            )
            json_response = response.json()

            if "response" in json_response:
                return json_response["response"]
            else:
                return str(json_response)

        except Exception as e:
            return f"Erro com modelo alternativo: {str(e)}"
