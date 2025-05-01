import os
from typing import Dict, List, Optional

import fitz  # PyMuPDF
from fastapi import UploadFile
from paddleocr import PaddleOCR


class OCRService:
    def __init__(self):
        # Inicializa o OCR uma única vez para economizar recursos
        self.ocr = PaddleOCR(use_angle_cls=True, lang="pt")

    async def extrair_texto_arquivos(self, arquivos: List[UploadFile]) -> List[str]:
        """Extrai texto de uma lista de arquivos PDF ou imagens."""
        resultados = []

        for arquivo in arquivos:
            try:
                # Salva o arquivo temporariamente para processamento
                temp_path = f"/tmp/{arquivo.filename}"
                with open(temp_path, "wb") as f:
                    content = await arquivo.read()
                    f.write(content)

                # Determina o tipo de arquivo e processa
                if arquivo.filename.lower().endswith('.pdf'):
                    texto = self._extrair_texto_pdf(temp_path)
                else:
                    texto = self._extrair_texto_imagem(temp_path)

                resultados.append(texto)

                # Limpa o arquivo temporário
                os.remove(temp_path)

            except Exception as e:
                print(f"Erro ao processar arquivo {arquivo.filename}: {e}")
                resultados.append(f"Erro ao processar arquivo: {str(e)}")

        return resultados

    def _extrair_texto_pdf(self, caminho_arquivo: str) -> str:
        """Extrai texto de um arquivo PDF usando OCR."""
        texto_completo = []

        try:
            # Abre o PDF
            doc = fitz.open(caminho_arquivo)

            # Extrai texto de cada página
            for pagina in doc:
                # Primeiro tenta extrair texto diretamente se disponível
                texto_pagina = pagina.get_text()

                # Se não houver texto suficiente, aplica OCR na imagem da página
                if len(texto_pagina.strip()) < 100:
                    pix = pagina.get_pixmap()
                    img_path = f"{caminho_arquivo}_page_{pagina.number}.png"
                    pix.save(img_path)

                    texto_pagina = self._extrair_texto_imagem(img_path)
                    os.remove(img_path)

                texto_completo.append(texto_pagina)

            return "\n\n".join(texto_completo)

        except Exception as e:
            print(f"Erro na extração de texto do PDF {caminho_arquivo}: {e}")
            return f"Erro na extração do texto: {str(e)}"

    def _extrair_texto_imagem(self, caminho_arquivo: str) -> str:
        """Extrai texto de uma imagem usando OCR."""
        try:
            resultado = self.ocr.ocr(caminho_arquivo, cls=True)

            if not resultado or not resultado[0]:
                return "Nenhum texto detectado na imagem."

            texto = []
            for linha in resultado[0]:
                if isinstance(linha, list) and len(linha) > 1:
                    texto.append(linha[1][0])  # Extrai o texto detectado

            return "\n".join(texto)

        except Exception as e:
            print(
                f"Erro na extração de texto da imagem {caminho_arquivo}: {e}")
            return f"Erro na extração do texto: {str(e)}"
