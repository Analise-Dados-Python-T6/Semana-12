import pandas as pd
from pathlib import Path
from banco import conectar, executar, inserir_em_lote
from config import ARQUIVOS


def localizar_zip():
    """Verifica se o arquivo cafeteria.zip foi extraído."""
    zip_path = Path('data/cafeteria.zip')

    if not zip_path.exists():
        print(f"❌ Arquivo não encontrado: {zip_path}")
        print("   Coloque 'cafeteria.zip' em 'data/' e extraia os CSVs")
        return False

    return True


def carregar_csv(tabela, arquivo_csv):
    """
    Lê um CSV e insere em uma tabela raw.

    Args:
        tabela: Nome da tabela no banco.
        arquivo_csv: Caminho do arquivo CSV.
    """
    conexao = conectar('cafeteria')

    if conexao is None:
        print(f"❌ Não foi possível conectar ao banco")
        return False

    try:
        # Passo 1: Limpar a tabela (TRUNCATE apaga tudo)
        print(f"  → Limpando tabela {tabela}...")
        executar(conexao, f"TRUNCATE TABLE {tabela}", commit=True)

        # Passo 2: Ler CSV em chunks (pedaços) para não consumir muita memória
        print(f"  → Lendo {arquivo_csv}...")
        chunk_size = 50000  # 50 mil linhas por vez

        total_linhas = 0
        for chunk in pd.read_csv(
            arquivo_csv,
            sep=';',
            encoding='latin-1',
            dtype=str,
            keep_default_na=False,
            chunksize=chunk_size
        ):
            # Passo 3: Inserir cada chunk
            if inserir_em_lote(conexao, tabela, chunk):
                total_linhas += len(chunk)
                print(f"    → {total_linhas} linhas inseridas...")

        print(f"✓ Tabela {tabela}: {total_linhas} linhas carregadas\n")
        return True

    except Exception as e:
        print(f"❌ Erro ao carregar {arquivo_csv}: {e}")
        return False
    finally:
        conexao.close()


# ===== INÍCIO DO SCRIPT =====

print("=" * 60)
print("FASE 1: EXTRAIR DADOS PARA RAW")
print("=" * 60 + "\n")

# Verificar se os CSVs existem
if not localizar_zip():
    print("❌ Fase 1 falhou!")
    exit(1)

# Carregar cada arquivo CSV
for csv_name, table_name in ARQUIVOS.items():
    csv_path = f"data/{csv_name}"
    print(f"Carregando {csv_name}...")

    if not Path(csv_path).exists():
        print(f"❌ Arquivo não encontrado: {csv_path}")
        exit(1)

    if not carregar_csv(table_name, csv_path):
        exit(1)

print("=" * 60)
print("✅ Fase 1 concluída com sucesso!")
print("=" * 60)
