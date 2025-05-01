FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    tesseract-ocr \
    # Dependências para o OpenCV
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxext6 \
    libx11-6 \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY app/ ./app/
COPY app.py .

# Cria diretório temporário para os arquivos OCR
RUN mkdir -p /tmp

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]