import json
import os
from datetime import datetime
from typing import List, Optional

from bson import ObjectId  # Importando ObjectId do bson
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from .llm import consultar_llm_local
from .ocr import extrair_texto_arquivos


# Classe para serializar ObjectId do MongoDB
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["fabio_db"]
logs_collection = db["logs"]

app = FastAPI()


@app.post("/analisar")
async def analisar_curriculos(
    arquivos: List[UploadFile] = File(...),
    query: Optional[str] = Form(None),
    request_id: str = Form(...),
    user_id: str = Form(...)
):
    textos = extrair_texto_arquivos(arquivos)
    resultados = []

    if query:
        for i, texto in enumerate(textos):
            prompt = f"""
Você é um especialista em RH. Avalie o currículo abaixo em relação aos requisitos:
"{query}"

Currículo:
{texto}

Responda se ele atende aos requisitos e justifique.

e me responda em portugues. (obrigatorio!)
"""
            resposta = consultar_llm_local(prompt)
            resultados.append(
                {"arquivo": arquivos[i].filename, "resposta": resposta})
    else:
        for i, texto in enumerate(textos):
            prompt = f"""
Resuma o currículo abaixo destacando as principais habilidades, experiências e qualificações:

Currículo:
{texto}
"""
            resumo = consultar_llm_local(prompt)
            resultados.append(
                {"arquivo": arquivos[i].filename, "resumo": resumo})

    log = {
        "request_id": request_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "resultado": resultados
    }
    logs_collection.insert_one(log)

    # Quando retornar o log, use o encoder personalizado
    return JSONResponse(
        content=json.loads(json.dumps(log, cls=JSONEncoder))
    )
