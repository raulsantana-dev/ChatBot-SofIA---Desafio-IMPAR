# --- ETAPA 1: BUILDER ---
FROM python:3.11 AS builder
WORKDIR /app


RUN pip install --no-cache-dir --prefix=/install torch --index-url https://download.pytorch.org/whl/cpu


RUN pip install --no-cache-dir --prefix=/install typing-extensions filelock

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . ./api


FROM python:3.11-slim
WORKDIR /app


COPY --from=builder /install /usr/local
COPY --from=builder /app/api ./api

ENV PYTHONPATH=/app/api

EXPOSE 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]