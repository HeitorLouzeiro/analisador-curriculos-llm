"""
Documentação para a rota de análise de currículos.
"""
EXEMPLO_QUERY = "Desenvolvedor Python com experiência em FastAPI, MongoDB e pelo menos 2 anos de experiência"

EXEMPLO_RESPOSTA_COM_QUERY = {
    "request_id": "e1f2a3b4-c5d6-7e8f-9a0b-1c2d3e4f5a6b",
    "user_id": "user123",
    "timestamp": "2025-05-01T14:30:45.123",
    "query": EXEMPLO_QUERY,
    "resultado": [
        {
            "arquivo": "curriculo_candidato1.pdf",
            "resposta": """
                O currículo atende parcialmente aos requisitos da vaga.

                O candidato possui sólida experiência com Python (3 anos) e conhecimento em FastAPI como mencionado no projeto de API RESTful que desenvolveu.

                No entanto, não há menção explícita de experiência com MongoDB, apenas com bancos SQL.

                O tempo total de experiência como desenvolvedor ultrapassa os 2 anos exigidos, com 3 anos em desenvolvimento Python.

                Recomendação: Candidato potencialmente adequado, mas recomenda-se verificar durante a entrevista o conhecimento em MongoDB.
            """,
            "resumo": "null"
        }
    ],
    "_id": "6462a8e94f6d7b2e30a1c2d3"
}

EXEMPLO_RESPOSTA_SEM_QUERY = {
    "_id": "7563b9f95e7c8d3f41b2d3e4",
    "request_id": "f6e5d4c3-b2a1-9e8d-7f6e-5d4c3b2a1e9f",
    "user_id": "user123",
    "timestamp": "2025-05-01T15:45:30.987",
    "query": "null",
    "resultado": [
        {
            "arquivo": "curriculo_candidato1.pdf",
            "resumo": """
            **Resumo do Curriculo de Heitor Garcez Martins Louzeiro**
            \n\n**Nome:** Heitor Garcez Martins Louzeiro

            \n\n**Experiência:

            **\n- Desenvolvedor Backend e Full Stack Freelance (Eventos):
            Criado um sistema de eventos acadêmicos com +900 certificados,
            utilizando Django, Bootstrap, Postgres, Heroku e Git.

            \n- Desenvolvedor Backend e Fullstack OKEAN Yachts (Embarcações):
            Participou do desenvolvimento de uma prova de conceito como
            desenvolvedor frontend, criando 4 páginas (Home, Login, Signup e Chat)

            \n\n**Habilidades:**

            \n- Desenvolvimento web com Django e Python
            \n- Conhecimento em Bootstrap, Postgres, Heroku e Git\
            \n- Experiência com OpenAI e Chat GPT
            \n- Automatização com Python e Selenium
            \n- Conhecimento em HTML, CSS e idiomas estrangeiros (Inglês básico)
            \n- Habilidades de liderança e trabalho em equipe"""
        }
    ]
}

# Dados da documentação
ANALISE_SUMMARY = "Analisa currículos"

ANALISE_DESCRIPTION = """
Extrai texto de currículos usando OCR e realiza análise com LLM.

# Modos de operação

1. ** Modo Análise(com query)**: Avalia o currículo com base nos requisitos da vaga fornecidos no parâmetro `query`
2. ** Modo Resumo(sem query)**: Gera um resumo estruturado do currículo extraindo informações chave

# Parâmetros obrigatórios

* **arquivos**: Um ou mais arquivos de currículo(PDF ou imagens)
* **user_id**: Identificador do usuário que está realizando a análise

# Parâmetros opcionais

* **query**: Requisitos da vaga para comparação(se omitido, gera resumo)
* **request_id**: Identificador customizado para rastreamento da solicitação

# Formatos de arquivo aceitos

PDF(.pdf) e imagens(.png, .jpg, .jpeg, .bmp, .tiff, .tif)
"""

ANALISE_RESPONSES = {
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
    422: {
        "description": "Erro de validação (arquivos inválidos ou parâmetros incorretos)",
        "content": {
            "application/json": {
                "example": {
                    "detail": "É necessário enviar pelo menos um arquivo de currículo para análise. Que seja PDF ou imagem."
                }
            }
        }
    },
    500: {
        "description": "Erro interno no processamento",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Ocorreu um erro inesperado no processamento da solicitação."
                }
            }
        }
    },
    503: {
        "description": "Serviço de LLM indisponível",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Erro ao processar solicitação: 503: Serviço de LLM indisponível: Modelo 'llama3.2' não encontrado"
                }
            }
        }
    }

}
