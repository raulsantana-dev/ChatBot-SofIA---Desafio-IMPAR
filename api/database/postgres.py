import psycopg2

def get_conn(retries=10, delay=3):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host="postgres",
                port=5432,
                dbname="ragdb",
                user="postgres",
                password="postgres"
            )
            return conn
        except OperationalError:
            print(f"Banco não pronto, tentando novamente em {delay}s... ({attempt+1}/{retries})")
            time.sleep(delay)
    raise OperationalError("Não foi possível conectar ao banco após várias tentativas")