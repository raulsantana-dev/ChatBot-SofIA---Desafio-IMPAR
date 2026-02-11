# --- ETAPA 1: BUILDER ---
FROM python:3.11 AS builder
WORKDIR /app

# 1. Instala PyTorch (CPU) NO LUGAR CERTO (--prefix=/install)
# A correção está aqui: adicionamos --prefix=/install
RUN pip install --no-cache-dir --prefix=/install torch --index-url https://download.pytorch.org/whl/cpu

# 2. Instala dependências extras que estavam faltando
RUN pip install --no-cache-dir --prefix=/install typing-extensions filelock

# 3. Instala os requisitos do arquivo
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . ./api

# --- ETAPA 2: FINAL ---
FROM python:3.11-slim
WORKDIR /app

# 4. Copia tudo que foi instalado (agora incluindo o torch)
COPY --from=builder /install /usr/local
COPY --from=builder /app/api ./api

# 5. Configura o caminho para o Python achar seus arquivos
ENV PYTHONPATH=/app/api

EXPOSE 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]