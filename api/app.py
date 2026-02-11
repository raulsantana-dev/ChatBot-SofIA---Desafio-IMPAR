from litestar import Litestar
from api.routes.chat import chat
from api.routes.scrape import scrape, executar_scrape

def startup():
    print("🔥 API iniciou")
    executar_scrape()

executar_scrape()
app = Litestar(
    route_handlers=[chat, scrape],
    on_startup=[startup]
)