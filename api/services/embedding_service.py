import requests

OLLAMA_URL = "http://ollama:11434/api/embeddings"

def gerar_embedding(texto: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": texto
        },
        timeout=300
    )

    return response.json()["embedding"]
