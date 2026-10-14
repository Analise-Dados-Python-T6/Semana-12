import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Dicionário com configurações do PostgreSQL
POSTGRES_CONFIG = {
    'host': os.environ.get('PG_HOST', 'localhost'),
    'port': os.environ.get('PG_PORT', '5432'),
    'user': os.environ.get('PG_USER', 'postgres'),
    'password': os.environ.get('PG_PASSWORD', 'senha123'),
    'dbname': os.environ.get('PG_DATABASE', 'postgres'),
}

# Dicionário mapeando CSVs para tabelas
ARQUIVOS = {
    'vendas.csv': 'raw_vendas',
    'itens.csv': 'raw_itens',
}
