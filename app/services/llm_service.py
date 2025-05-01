import time
from typing import Optional

import requests


class LLMService:
    def __init__(self, base_url="http://ollama:11434"):
        self.base_url = base_url
        self.default_model = "llama3.2"
        self.fallback_model = "phi"
        self.default_temperature = 0.4

    def criar_prompt_analise(self, texto: str, query: str) -> str:
        """Cria um prompt para análise de currículo com requisitos específicos."""
        return f"""
                    Você é um especialista em Recursos Humanos com experiência em análise de currículos e recrutamento por competências.

                    Avalie o currículo abaixo com base nos seguintes requisitos da vaga: "{query}"

                    Currículo do candidato:
                    {texto}

                    Sua tarefa:

                    Diga se o currículo atende (ou não) aos requisitos que veio da query.

                    Justifique sua resposta com base nas informações presentes no currículo.

                    Importante:

                    A resposta deve estar em português.

                    Seja objetivo, mas forneça detalhes suficientes para embasar sua avaliação.

                    Considere experiência profissional, formação acadêmica, habilidades técnicas e comportamentais, quando aplicável.
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
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": self.default_temperature
                }

            )
            json_response = response.json()

            # Verifica se há erro de memória
            if "error" in json_response and "memory" in json_response["error"].lower():
                print(
                    f"Erro de memória com modelo {model}. Tentando com modelo menor...")
                return self._tentar_com_modelo_alternativo(prompt)

            # Lidando com diferentes formatos de resposta
            json_response = response.json()

            if "response" in json_response:
                return json_response["response"]
            else:
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
                json={
                    "model": self.fallback_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": self.default_temperature
                }

            )
            json_response = response.json()

            if "response" in json_response:
                return json_response["response"]
            else:
                return str(json_response)

        except Exception as e:
            return f"Erro com modelo alternativo: {str(e)}"
