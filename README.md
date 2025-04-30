# Fabio LLM OCR App

Sistema inteligente para análise de currículos com OCR + LLM local + API FastAPI

## Estrutura do projeto

```
app.py             # Ponto de entrada para execução local (opcional)
Dockerfile         # Configurações para criação da imagem Docker
requirements.txt   # Dependências do projeto
docker-compose.yml # Orquestração dos serviços
app/
  __init__.py      # Inicialização do pacote
  main.py          # API FastAPI
  ocr.py           # Funcionalidade de OCR
  llm.py           # Integração com modelo de linguagem local
```

## Instalação e execução

### Com Docker (recomendado)

1. Certifique-se de ter Docker e Docker Compose instalados
2. Clone o repositório
3. Execute:

```bash
docker-compose up --build
```

4. Após iniciar o container Ollama, execute:
```bash
docker exec fabio_ollama ollama pull mistral
```

### Acesso aos serviços

- API: http://localhost:8000/docs
- MongoDB: localhost:27017
- Ollama: http://localhost:11434

## Como usar

1. Acesse a documentação interativa da API em http://localhost:8000/docs
2. Use o endpoint `/analisar` para enviar currículos e obter análises
3. Forneça os parâmetros:
   - `arquivos`: Arquivos PDF ou imagens com currículos
   - `query`: (Opcional) Requisitos para análise
   - `request_id`: Identificador da requisição
   - `user_id`: Identificador do usuário

## Desenvolvimento local

Para executar o projeto localmente sem Docker:

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Certifique-se de ter MongoDB e Ollama em execução
3. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```