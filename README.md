# 🧠 Chatbot RAG Local com Memória e Upload de Documentos

## 📌 Visão Geral

Este projeto implementa um **chatbot AI local com RAG (Retrieval Augmented Generation)** capaz de responder perguntas com base em:

- Documentos enviados (PDF, CSV, Excel)  
- Conteúdo da web via scraping  
- Memória da conversa  
- Pesquisa vetorial com PGVector  
- LLM local via Ollama  

Tudo roda **100% local usando Docker Compose**, sem depender de APIs externas.

## 🏗 Arquitetura

Usuário (n8n Chat) → Requisição HTTP → API Python (Litestar)  

Serviços e funcionalidades da API:

- Embeddings (Ollama local)  
- PGVector (PostgreSQL)  
- Recuperação RAG  
- Memória da Conversa  
- Resposta via LLM (Ollama)  

Serviços do projeto:

- **n8n** → Interface de chat e orquestração  
- **api** → Backend (Litestar + LangChain)  
- **postgres** → Banco vetorial com PGVector  
- **ollama** → LLM local e embeddings  
- **adminer** → Interface de banco  

## 🚀 Funcionalidades

### Chat

- Suporte a múltiplos usuários  
- Memória de conversa por usuário  
- Respostas contextuais  
- LLM totalmente local  

### Upload de Documentos

- Suporta PDF, CSV e Excel  
- Fluxo:
  1. Enviar arquivo pelo chat (n8n)  
  2. Extrair texto  
  3. Gerar embeddings localmente  
  4. Armazenar no PostgreSQL (PGVector)  
  5. Usado para busca semântica  

### Web Scraping

- Endpoint: `POST /scrape`  
- Rastreia URL configurada  
- Limpa HTML e converte em texto  
- Gera embeddings  
- Armazena em PGVector  

## 🧠 Memória

Memória de curto prazo por usuário, permitindo contexto independente

## 🗂 Estrutura do Projeto

- api/
  - routes/
    - chat.py
    - scrape.py
  - services/
    - rag_service.py
    - memory_service.py
    - embedding_service.py
  - database/
    - postgres.py
  - app.py
- docker-compose.yml
- Dockerfile
- requirements.txt
- README.md

## 🐳 Executando Localmente

1. Clonar repositório:

bash
git clone <https://github.com/raulsantana-dev/ChatBot-SofIA---Desafio-IMPAR>
cd chatbot-rag

2. Subir os serviços:
docker compose up 

3. Baixar modelos Ollama:

docker exec -it ollama ollama pull llama3
docker exec -it ollama ollama pull nomic-embed-text

## 💬 Endpoints Principais
POST /chat

Enviar mensagem ou arquivo.

Exemplo de texto:

{
  "message": "O que é inteligência artificial?",
  "user_id": "raul"
}


Exemplo com arquivo:
Enviar via multipart/form-data com campos: message, user_id, file.

POST /scrape

Dispara scraping e armazenamento de embeddings:

POST http://localhost:8000/scrape


## 👨‍💻 Autor

Desenvolvido por Raul Santana Santos de Araujo como parte do Desafio Técnico proposto pela IMPAR.