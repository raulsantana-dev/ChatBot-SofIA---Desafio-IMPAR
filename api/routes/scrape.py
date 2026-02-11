from litestar import post
import requests
from bs4 import BeautifulSoup
from api.services.embedding_service import gerar_embedding
from api.database.postgres import get_conn
import os

SCRAPE_URL = os.getenv(
    "SCRAPE_URL",
    "https://pt.wikipedia.org/wiki/Intelig%C3%AAncia_artificial"
)

def executar_scrape():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM documents")
    total = cur.fetchone()[0]

    if total > 20:
        print("📚 Base já populada. Pulando scraping.")
        cur.close()
        conn.close()
        return
    print("\n==============================")
    print("🚀 INICIANDO SCRAPING AUTO")
    print("URL:", SCRAPE_URL)
    print("==============================\n")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(SCRAPE_URL, headers=headers, timeout=60)
        soup = BeautifulSoup(res.text, "html.parser")

        paragrafos = soup.find_all("p")
        textos = []

        for p in paragrafos:
            texto = p.get_text().strip()
            if len(texto) > 80:
                textos.append(texto)

        print(f"📄 textos coletados: {len(textos)}")

        if not textos:
            print("⚠️ nada encontrado")
            return

        conn = get_conn()
        cur = conn.cursor()

        salvos = 0

        for texto in textos:
            try:
                embedding = gerar_embedding(texto)

                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                    (texto, embedding)
                )

                salvos += 1
            except Exception as e:
                print("❌ erro:", e)

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ scraping salvo: {salvos}")

    except Exception as e:
        print("💥 ERRO SCRAPE:", e)



@post("/scrape")
async def scrape() -> dict:
    executar_scrape()
    return {"status": "scraping executado"}
