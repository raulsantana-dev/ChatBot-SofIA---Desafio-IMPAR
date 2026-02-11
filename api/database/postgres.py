import os
import time
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

def get_conn(retries=10, delay=3):
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = int(os.getenv("POSTGRES_PORT", 5432))
    dbname = os.getenv("POSTGRES_DB", "ragdb")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")

    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            return conn
        except OperationalError:
            print(f"Banco não pronto, tentando novamente em {delay}s... ({attempt+1}/{retries})")
            time.sleep(delay)
    raise OperationalError("Não foi possível conectar ao banco após várias tentativas")
