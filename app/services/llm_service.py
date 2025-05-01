from typing import Optional

import requests


class ModelNotFoundException(Exception):
    """Exceção lançada quando o modelo LLM requisitado não está disponível."""
    pass


class LLMService:
    def __init__(self, base_url="http://ollama:11434"):
        self.base_url = base_url
        self.default_model = "llama3.2"
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

            # Verificar se há erro de modelo não encontrado
            if "error" in json_response:
                error_msg = str(json_response["error"]).lower()
                if "not found" in error_msg:
                    raise ModelNotFoundException(
                        f"Modelo '{model}' não encontrado")
                elif "memory" in error_msg:
                    return (f"Erro de memória com modelo {model}. "
                            f"Por favor, baixe um modelo mais leve para o seu ambiente Docker "
                            f"usando 'docker exec -it ollama-container ollama pull [modelo-leve]' "
                            f"e tente novamente.")

            # Lidando com diferentes formatos de resposta
            if "response" in json_response:
                return json_response["response"]
            else:
                return str(json_response)

        except ModelNotFoundException:
            # Repropagar a exceção para ser tratada no nível superior
            raise
        except Exception as e:
            print(f"Erro ao consultar LLM: {e}")
            return f"Erro: {str(e)}"
