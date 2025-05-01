"""
Ponto de entrada para execução local do projeto Fabio LLM OCR
Este arquivo permite executar o projeto diretamente sem Docker
"""

import uvicorn

if __name__ == "__main__":
    # Execute o servidor com reload ativado para desenvolvimento
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
