🧠 Chatbot RAG Local com Memória e Upload de Documentos
📌 Visão Geral

Este projeto implementa um chatbot AI local com RAG (Retrieval Augmented Generation) capaz de responder perguntas com base em:

Documentos enviados (PDF, CSV, Excel)

Conteúdo da web via scraping

Memória da conversa

Pesquisa vetorial com PGVector

LLM local via Ollama

Tudo roda 100% local usando Docker Compose, sem depender de APIs externas.

🏗 Arquitetura
Usuário (n8n Chat)
      ↓
Requisição HTTP
      ↓
API Python (Litestar)
      ↓
- Embeddings (Ollama local)
- PGVector (PostgreSQL)
- Recuperação RAG
- Memória da Conversa
- Resposta via LLM (Ollama)


Serviços:

n8n → Interface de chat e orquestração

api → Backend (Litestar + LangChain)

postgres → Banco vetorial com PGVector

ollama → LLM local e embeddings

adminer → Interface de banco

🚀 Funcionalidades
Chat

Suporte a múltiplos usuários

Memória de conversa por usuário

Respostas contextuais

LLM totalmente local

Upload de Documentos

Suporta:

PDF

CSV

Excel

Fluxo:

Enviar arquivo pelo chat (n8n)

Extrair texto

Gerar embeddings localmente

Armazenar no PostgreSQL (PGVector)

Usado para busca semântica

Web Scraping

Endpoint:

POST /scrape


Rastreia URL configurada

Limpa HTML e converte em texto

Gera embeddings

Armazena em PGVector

🧠 Memória

Memória de curto prazo por usuário, permitindo contexto independente:

user_id = "raul"
user_id = "joao"
user_id = "empresa_x"


Permite perguntas de acompanhamento como:

"Explique melhor"
"Resuma isso"
"O que eu enviei antes?"

🗂 Estrutura do Projeto
chatbot-rag/
│
├── api/
│   ├── routes/
│   │   ├── chat.py
│   │   └── scrape.py
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── memory_service.py
│   │   ├── embedding_service.py
│   │   └── file_service.py
│   │
│   ├── database/
│   │   └── postgres.py
│   │
│   └── app.py
│
├── docker-compose.yml
├── Dockerfile
└── requirements.txt

🐳 Executando Localmente
1. Clonar repositório
git clone <repo>
cd chatbot-rag

2. Subir os serviços
docker compose up --build


URLs:

Serviço	URL
API	http://localhost:8000

n8n	http://localhost:5678

Adminer	http://localhost:8080

Ollama	http://localhost:11434
🤖 Modelos

Após iniciar os containers:

docker exec -it ollama ollama pull llama3
docker exec -it ollama ollama pull nomic-embed-text

💬 Endpoints Principais
POST /chat

Enviar mensagem ou arquivo.

Texto:

{
  "message": "O que é inteligência artificial?",
  "user_id": "raul"
}


Com arquivo:
Enviar via multipart/form-data com campos: message, user_id, file.

POST /scrape

Dispara scraping e armazenamento de embeddings:

POST http://localhost:8000/scrape

🧪 Exemplo curl

Chat:

curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message":"O que é IA?","user_id":"raul"}'


Upload de arquivo:

curl -X POST http://localhost:8000/chat \
-F "message=Resuma este documento" \
-F "user_id=raul" \
-F "file=@file.pdf"

👨‍💻 Autor

Desenvolvido por Raul Santana Santos de Araujo como parte do Desafio Técnico proposto pela IMPAR.
