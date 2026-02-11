from api.services.embedding_service import gerar_embedding
from api.services.memory_service import get_memory, salvar_memoria
from api.database.postgres import get_conn
import requests


def buscar_contexto_relevante(embedding_pergunta, limit=5):
    """
    Busca os 5 trechos mais parecidos com a pergunta no banco de dados.
    """
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    SELECT content 
    FROM documents 
    ORDER BY embedding <=> %s::vector 
    LIMIT %s
    """
    
    cur.execute(sql, (embedding_pergunta, limit))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()

    
    contexto = "\n\n".join([row[0] for row in rows])
    return contexto

def buscar_contexto(embedding):

    conn = get_conn()
    cur = conn.cursor()

    # transforma lista em formato vector do postgres
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    cur.execute(
        f"""
        SELECT content
        FROM documents
        ORDER BY embedding <-> '{embedding_str}'::vector
        LIMIT 4
        """
    )

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    textos = [r[0] for r in resultados]
    return "\n".join(textos)



def gerar_resposta(pergunta: str, user_id: str = "default"):

    print("\n🧠 GERANDO RESPOSTA RAG")
    print("Usuário:", user_id)
    print("Pergunta:", pergunta)
    pergunta_embedding = gerar_embedding(pergunta)
    print("🔢 embedding pergunta OK")
    contexto_conversa = buscar_contexto(pergunta_embedding)
    contexto_geral = (pergunta_embedding)
    print("📚 contexto encontrado")
    memoria = get_memory(user_id)
    print("💬 memoria carregada:", memoria)

    prompt = f"""
Você é um assistente de IA corporativo.

Use o contexto abaixo para responder a pergunta do usuário.
Se a resposta não estiver no contexto, use seu conhecimento geral.
INFORMAÇÕES DO USUÁRIO:
    - NÃO confunda o seu nome com o nome do usuário. Você é a SofIA.

HISTÓRICO DA CONVERSA: {memoria}

CONTEXTO DOS DOCUMENTOS: {contexto_geral}

CONTEXTO DA CONVERSA: {contexto_conversa}

PERGUNTA DO USUÁRIO: {pergunta}

Responda de forma clara e profissional.
"""

    # chamada ollama
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    resposta = response.json()["response"]

    print("🤖 resposta gerada")

    # salva memória da conversa
    salvar_memoria(user_id, pergunta, resposta)
    print("💾 memoria salva")

    return resposta
