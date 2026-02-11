from litestar import Litestar
from api.routes.chat import chat
from api.routes.scrape import scrape, executar_scrape

def startup():
    print("🔥 API iniciou - Verificando Scrape...")
    try:
        executar_scrape()
    except Exception as e:
        print(f"Erro no startup scrape: {e}")


app = Litestar(
    route_handlers=[chat, scrape],
    on_startup=[startup]
)