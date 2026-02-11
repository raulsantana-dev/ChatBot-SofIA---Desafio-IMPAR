from litestar import post, Request
from api.services.rag_service import gerar_resposta
from api.services.embedding_service import gerar_embedding
from api.database.postgres import get_conn

import pdfplumber
import pandas as pd
import io

@post("/chat")
async def chat(request: Request) -> dict:
    try:
        form = await request.form()

        pergunta = form.get("message", "")
        user_id = form.get("user_id", "user1")
        arquivo = form.get("file")

        texto_extraido = ""

       
        if arquivo:
            filename = arquivo.filename.lower()
            content = await arquivo.read()

            # PDF
            if filename.endswith(".pdf"):
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    for page in pdf.pages:
                        texto_extraido += page.extract_text() or ""

            # CSV
            elif filename.endswith(".csv"):
                df = pd.read_csv(io.BytesIO(content))
                texto_extraido = df.to_string()

            # EXCEL
            elif filename.endswith(".xlsx") or filename.endswith(".xls"):
                df = pd.read_excel(io.BytesIO(content))
                texto_extraido = df.to_string()

            else:
                return {"erro": "formato não suportado"}

      
        texto_final = f"{pergunta}\n{texto_extraido}".strip()

        if not texto_final:
            return {"erro": "mensagem vazia"}

        print("USER:", user_id)
        print("TEXTO:", texto_final[:200])

        embedding = gerar_embedding(texto_final)

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (texto_final, embedding)
        )

        conn.commit()
        cur.close()
        conn.close()

        resposta = gerar_resposta(texto_final, user_id)

        return {"resposta": resposta}

    except Exception as e:
        print("ERRO REAL:", e)
        return {"erro": str(e)}
