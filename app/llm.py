import time

import requests


def consultar_llm_local(prompt: str, model="tinyllama"):
    # Usa tinyllama como modelo padrão por exigir menos memória
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    json_response = response.json()

    # Verifica se há erro de memória
    if "error" in json_response and "memory" in json_response["error"].lower():
        print(
            f"Erro de memória com modelo {model}. Tentando com modelo ainda menor...")

        # Se mesmo o tinyllama falhar, tenta com um modelo ainda menor
        try:
            # Baixa o modelo menor se necessário
            requests.post(
                "http://ollama:11434/api/pull",
                json={"model": "phi"}
            )
            time.sleep(2)  # Espera um pouco para o modelo ser carregado

            # Tenta novamente com o modelo menor
            response = requests.post(
                "http://ollama:11434/api/generate",
                json={"model": "phi", "prompt": prompt, "stream": False}
            )
            json_response = response.json()
        except Exception as e:
            print(f"Erro ao tentar modelo alternativo: {e}")
            return f"Erro: Não foi possível processar a solicitação devido a limitações de memória. {str(e)}"

    # Lidando com diferentes formatos de resposta possíveis
    if "response" in json_response:
        return json_response["response"]
    elif "response_data" in json_response:
        return json_response["response_data"]
    elif "generation" in json_response:
        return json_response["generation"]
    elif "error" in json_response:
        return f"Erro do modelo: {json_response['error']}"
    else:
        # Registra a estrutura completa da resposta para depuração
        print(f"Estrutura da resposta: {json_response}")
        # Retorna o texto completo da resposta como fallback
        return str(json_response)
