import io

from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes
from PIL import Image

ocr_engine = PaddleOCR(use_angle_cls=True, lang='pt', )


def extrair_texto_arquivos(arquivos):
    textos = []
    for file in arquivos:
        if file.filename.lower().endswith(".pdf"):
            imagens = convert_from_bytes(file.file.read())
        else:
            imagens = [Image.open(file.file)]

        texto_total = ""
        for img in imagens:
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            resultado = ocr_engine.ocr(img_bytes.getvalue(), cls=True)
            for linha in resultado[0]:
                texto_total += linha[1][0] + "\n"

        textos.append(texto_total.strip())
    return textos
