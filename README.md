# Roteiro Completo: Configuração e Execução do Pipeline Cafeteria

**PostgreSQL + Python | Módulo 1 - Semana 10**

---

## Introdução

Este roteiro guia você passo a passo pela configuração completa do ambiente e pela execução de um pipeline de dados real, usando PostgreSQL e Python. Vamos desde a instalação das ferramentas até a análise final dos dados. Cada comando será explicado em detalhes, assumindo que você nunca usou essas ferramentas antes.

**Referência de dados:** 30/09/2025 (use esta data em todas as queries para resultados determinísticos).

---

## PARTE 1: PRÉ-REQUISITOS E VERIFICAÇÕES

### 1.1 Verificar o Sistema Operacional

Antes de começar, você precisa saber qual sistema operacional (SO) está usando:

**No Windows:**
- Abra o PowerShell (clique no ícone do Windows e digite "PowerShell")
- Escreva: `Get-ComputerInfo | Select-Object CsSystemType`
- Você verá "x64-based PC" ou similar

**No macOS ou Linux:**
- Abra o Terminal
- Escreva: `uname -m`
- Você verá "x86_64", "arm64" ou similar

### 1.2 Verificar se Python já está instalado

Python é uma linguagem de programação. Vamos checar se você já o tem:

**No Windows (PowerShell):**
```powershell
python --version
```

**No macOS ou Linux (Terminal):**
```bash
python3 --version
```

Se a resposta for "Python 3.10" ou maior, ótimo! Pule para a seção 2 (PostgreSQL). Caso contrário, siga a instalação abaixo.

---

## PARTE 2: INSTALAR POSTGRESQL 13+

PostgreSQL é um banco de dados relacional. É onde vamos armazenar os dados do nosso pipeline.

### 2.1 Download e Instalação

**No Windows:**
1. Acesse https://www.postgresql.org/download/windows/
2. Clique em "Interactive installer by EDB"
3. Baixe a versão 13, 14 ou 15 (qualquer uma funciona)
4. Execute o instalador (.exe)
5. Na tela "Password", defina uma senha para o usuário `postgres` (ex: "senha123")
   - **Anote esta senha!** Você usará depois.
6. Na tela "Port", deixe como 5432 (padrão)
7. Clique "Next" até o final

**No macOS:**
```bash
brew install postgresql@13
brew services start postgresql@13
```

**No Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
```

### 2.2 Verificar a Instalação

**No Windows (PowerShell):**
```powershell
psql --version
```

**No macOS ou Linux (Terminal):**
```bash
psql --version
```

Você deve ver algo como "psql (PostgreSQL) 13.x" ou superior.

---

## PARTE 3: INSTALAR PYTHON 3.10+

Se você já tem Python 3.10+, pule para a seção 4.

### 3.1 Download e Instalação

**No Windows:**
1. Acesse https://www.python.org/downloads/
2. Clique em "Download Python 3.11" (ou versão mais recente)
3. Execute o instalador (.exe)
4. **IMPORTANTE:** Marque a caixa "Add Python to PATH" (antes de clicar "Install Now")
5. Clique "Install Now"
6. Aguarde a conclusão

**No macOS:**
```bash
brew install python@3.11
```

**No Linux (Ubuntu/Debian):**
```bash
sudo apt install python3.11 python3.11-venv python3-pip -y
```

### 3.2 Verificar a Instalação

Feche e reabra o PowerShell/Terminal, depois escreva:

```bash
python --version
```

Deve aparecer "Python 3.10" ou superior.

---

## PARTE 4: CRIAR PASTA DO PROJETO

Vamos criar uma pasta onde todos os arquivos ficarão organizados.

**No Windows (PowerShell):**
```powershell
mkdir C:\Users\seu_usuario\Desktop\cafeteria-pipeline
cd C:\Users\seu_usuario\Desktop\cafeteria-pipeline
```

**No macOS ou Linux (Terminal):**
```bash
mkdir ~/cafeteria-pipeline
cd ~/cafeteria-pipeline
```

Confirme que você está na pasta certa escrevendo:
```bash
pwd
```

---

## PARTE 5: CRIAR AMBIENTE VIRTUAL PYTHON

Um ambiente virtual é como uma "caixa isolada" onde você instala as dependências de um projeto. Cada projeto tem seu próprio ambiente, evitando conflitos.

### 5.1 Criar o Ambiente

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No macOS ou Linux (Terminal):**
```bash
python3 -m venv venv
source venv/bin/activate
```

Você saberá que o ambiente está ativo quando a linha de comando mostrar `(venv)` no início.

### 5.2 Atualizar o pip

O pip é o gerenciador de pacotes do Python (ele baixa e instala bibliotecas):

```bash
python -m pip install --upgrade pip
```

---

## PARTE 6: INSTALAR DEPENDÊNCIAS PYTHON

Agora vamos instalar as bibliotecas que nossos scripts precisam:

```bash
pip install pandas sqlalchemy psycopg2-binary matplotlib python-dotenv jupyter
```

**O que cada pacote faz:**

- **pandas**: Lê e manipula arquivos CSV (Excel em formato texto)
- **sqlalchemy**: Permite que Python "fale" com o PostgreSQL
- **psycopg2-binary**: Driver que conecta Python ao PostgreSQL
- **matplotlib**: Cria gráficos
- **python-dotenv**: Lê arquivos `.env` (senhas e configurações)
- **jupyter**: Ferramenta para rodar análises em Python

A instalação pode levar 1-2 minutos. Aguarde até ver `Successfully installed...`.

---

## PARTE 7: CRIAR ARQUIVO DE CONFIGURAÇÃO (.env)

O arquivo `.env` armazena suas credenciais do PostgreSQL (senha, usuário, etc.). **Nunca compartilhe este arquivo.**

### 7.1 Abrir Editor de Texto

**No Windows:**
- Abra o Bloco de Notas (digitando "Notepad" no menu Iniciar)

**No macOS ou Linux:**
- Abra o Terminal e escreva: `nano .env`

### 7.2 Escrever as Credenciais

Cole o seguinte conteúdo (substituindo "senha123" pela senha que você criou no passo 2.1):

```env
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=senha123
PG_DATABASE=cafeteria
```

**Explicação:**
- `PG_HOST=localhost`: O PostgreSQL está rodando neste computador
- `PG_PORT=5432`: Porta padrão do PostgreSQL
- `PG_USER=postgres`: Usuário padrão criado na instalação
- `PG_PASSWORD`: A senha que você definiu na instalação
- `PG_DATABASE`: Nome do banco que vamos criar (será criado automaticamente)

### 7.3 Salvar o Arquivo

**No Bloco de Notas (Windows):**
- Clique "Arquivo" → "Salvar Como"
- Navegue até a pasta do projeto
- Nome: `.env`
- Tipo: "Todos os arquivos (.)"
- Clique "Salvar"

**No nano (macOS/Linux):**
- Pressione `Ctrl+O`, depois `Enter`
- Pressione `Ctrl+X` para sair

---

## PARTE 8: CRIAR ARQUIVOS DE CONFIGURAÇÃO PYTHON

Agora vamos criar os scripts Python que controlam tudo.

### 8.1 Arquivo `config.py`

Este arquivo lê o `.env` e oferece as configurações para todos os outros scripts.

**No Windows (PowerShell):**
```powershell
# Abra o Bloco de Notas e salve em config.py
```

**No Terminal (qualquer SO):**
```bash
nano config.py
```

**Conteúdo de `config.py`:**

```python
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
    'dbname': os.environ.get('PG_DATABASE', 'cafeteria'),
}

# Dicionário mapeando CSVs para tabelas
ARQUIVOS = {
    'vendas.csv': 'raw_vendas',
    'itens.csv': 'raw_itens',
}
```

**Explicação:**
- `load_dotenv()`: Lê o arquivo `.env` e carrega as variáveis
- `os.environ.get()`: Pega uma variável de ambiente (do `.env`) ou usa um valor padrão
- `POSTGRES_CONFIG`: Dicionário com informações de conexão
- `ARQUIVOS`: Mapeia cada CSV a sua tabela no banco

Salve o arquivo (Ctrl+S no nano).

### 8.2 Arquivo `banco.py`

Este arquivo gerencia a conexão com o PostgreSQL.

**Conteúdo de `banco.py`:**

```python
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import POSTGRES_CONFIG
import pandas as pd

def motor(dbname=None):
    """
    Cria uma conexão SQLAlchemy com o PostgreSQL.
    
    Args:
        dbname: Nome do banco. Se None, conecta ao banco 'postgres' (padrão).
    
    Returns:
        engine: Objeto SQLAlchemy Engine.
    """
    if dbname is None:
        dbname = 'postgres'  # Banco padrão do PostgreSQL
    
    url = (
        f"postgresql+psycopg2://"
        f"{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}"
        f"@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{dbname}"
    )
    
    try:
        engine = create_engine(url)
        return engine
    except Exception as e:
        print(f"Erro ao criar engine: {e}")
        return None

def conectar(dbname='cafeteria'):
    """
    Abre uma conexão com o PostgreSQL e retorna o objeto Connection.
    
    Args:
        dbname: Nome do banco (padrão: 'cafeteria').
    
    Returns:
        Connection: Conexão aberta, ou None se falhar.
    """
    try:
        engine = motor(dbname)
        conexao = engine.connect()
        return conexao
    except SQLAlchemyError as e:
        print(f"❌ Erro ao conectar ao PostgreSQL:")
        print(f"   Host: {POSTGRES_CONFIG['host']}")
        print(f"   Porta: {POSTGRES_CONFIG['port']}")
        print(f"   Usuário: {POSTGRES_CONFIG['user']}")
        print(f"   Banco: {dbname}")
        print(f"   Mensagem: {e.orig}")
        return None

def executar(conexao, sql, commit=True):
    """
    Executa um comando SQL (INSERT, DELETE, UPDATE, CREATE, etc.).
    
    Args:
        conexao: Objeto Connection aberto.
        sql: String com o SQL a executar.
        commit: Se True, faz commit automático. Se False, precisa fazer commit manualmente.
    
    Returns:
        True se sucesso, False se erro.
    """
    try:
        conexao.execute(text(sql))
        if commit:
            conexao.commit()
        return True
    except SQLAlchemyError as e:
        print(f"❌ Erro ao executar SQL: {e.orig}")
        conexao.rollback()
        return False

def consultar(sql, conexao):
    """
    Executa uma query SELECT e retorna os resultados em um DataFrame pandas.
    
    Args:
        sql: String com a query SELECT.
        conexao: Objeto Connection aberto.
    
    Returns:
        DataFrame com os resultados.
    """
    try:
        df = pd.read_sql(text(sql), conexao, coerce_float=True)
        return df
    except SQLAlchemyError as e:
        print(f"❌ Erro ao consultar: {e.orig}")
        return None

def inserir_em_lote(conexao, tabela, dataframe):
    """
    Insere um DataFrame inteiro em uma tabela, em lotes de 1000 linhas.
    
    Args:
        conexao: Objeto Connection aberto.
        tabela: Nome da tabela.
        dataframe: DataFrame a inserir.
    
    Returns:
        True se sucesso, False se erro.
    """
    try:
        dataframe.to_sql(
            tabela,
            conexao,
            if_exists='append',
            method='multi',
            chunksize=1000,
            index=False
        )
        conexao.commit()
        return True
    except SQLAlchemyError as e:
        print(f"❌ Erro ao inserir em lote: {e.orig}")
        conexao.rollback()
        return False
```

**Explicação das funções:**

- **`motor(dbname)`**: Cria um "motor" SQLAlchemy que sabe como falar com PostgreSQL. A URL contém user, password, host e port.

- **`conectar()`**: Abre uma conexão real com o banco. Se falhar, mostra um erro amigável.

- **`executar()`**: Roda comandos como `INSERT`, `DELETE`, `UPDATE`, `CREATE TABLE`.

- **`consultar()`**: Roda `SELECT` e retorna os dados como um DataFrame pandas (tabela em Python).

- **`inserir_em_lote()`**: Insere muitas linhas rapidamente, dividindo em grupos de 1000.

Salve o arquivo.

---

## PARTE 9: PREPARAR OS DADOS

### 9.1 Obter o arquivo `cafeteria.zip`

O arquivo `cafeteria.zip` contém dois CSVs com dados de vendas da cafeteria:
- `vendas.csv`: 150 vendas (pedidos)
- `itens.csv`: 491 itens de venda (produtos em cada pedido)

**Se você não tem este arquivo:**
- Crie uma pasta `data` na raiz do projeto: `mkdir data`
- Coloque o arquivo `cafeteria.zip` lá

**Se você tem o arquivo:**
- Coloque-o em `data/cafeteria.zip`

### 9.2 Extrair o ZIP

**No Windows (PowerShell):**
```powershell
Expand-Archive -Path data\cafeteria.zip -DestinationPath data\
```

**No Terminal (macOS/Linux):**
```bash
unzip data/cafeteria.zip -d data/
```

Você deve ver agora:
```
data/
  ├── vendas.csv
  └── itens.csv
```

---

## PARTE 10: FASE 0 - CRIAR BANCO E TABELAS

Esta fase cria o banco de dados e define a estrutura das tabelas (como um "molde").

### 10.1 Criar o arquivo `0_criar_banco.sql`

Este arquivo contém os comandos SQL puros (sem Python). É a "receita" para criar as tabelas.

**Conteúdo de `0_criar_banco.sql`:**

```sql
-- =====================================================================
-- Criação do banco de dados e tabelas para o pipeline Cafeteria
-- =====================================================================

-- DROP DATABASE IF EXISTS cafeteria;
-- CREATE DATABASE cafeteria ENCODING 'UTF8';

-- =====================================================================
-- TABELAS RAW (dados brutos do CSV, tudo como texto)
-- =====================================================================

DROP TABLE IF EXISTS raw_itens CASCADE;
DROP TABLE IF EXISTS raw_vendas CASCADE;

CREATE TABLE raw_vendas (
    id_venda VARCHAR(10),
    data_pedido VARCHAR(10),
    data_entrega VARCHAR(10),
    nome_loja VARCHAR(50),
    id_cliente VARCHAR(10),
    valor_bruto VARCHAR(20),
    valor_desconto VARCHAR(20)
);

CREATE TABLE raw_itens (
    id_venda VARCHAR(10),
    sequencia_item VARCHAR(5),
    produto VARCHAR(50),
    categoria VARCHAR(20),
    quantidade VARCHAR(5),
    preco_unitario VARCHAR(20)
);

-- =====================================================================
-- TABELAS SILVER (dados limpos e convertidos para tipos corretos)
-- =====================================================================

DROP TABLE IF EXISTS silver_itens CASCADE;
DROP TABLE IF EXISTS silver_vendas CASCADE;

CREATE TABLE silver_vendas (
    id_venda INT PRIMARY KEY,
    data_pedido DATE NOT NULL,
    data_entrega DATE NOT NULL,
    nome_loja VARCHAR(50) NOT NULL,
    id_cliente INT,
    valor_bruto NUMERIC(10, 2),
    valor_desconto NUMERIC(10, 2),
    valor_total NUMERIC(10, 2),
    prazo_dias INT,
    CHECK (valor_bruto >= 0),
    CHECK (valor_desconto >= 0),
    CHECK (prazo_dias >= 0)
);

CREATE TABLE silver_itens (
    id_item SERIAL PRIMARY KEY,
    id_venda INT NOT NULL,
    sequencia_item INT NOT NULL,
    produto VARCHAR(50) NOT NULL,
    categoria VARCHAR(20) NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario > 0),
    subtotal NUMERIC(10, 2),
    FOREIGN KEY (id_venda) REFERENCES silver_vendas(id_venda),
    UNIQUE(id_venda, sequencia_item)
);
```

**Explicação:**

- **DROP TABLE IF EXISTS**: Apaga a tabela se ela já existe (para poder rodar o script múltiplas vezes).
- **raw_vendas / raw_itens**: Tabelas com dados brutos (tudo VARCHAR = texto).
- **silver_vendas / silver_itens**: Tabelas com dados limpos e com tipos corretos (INT, DATE, NUMERIC).
- **PRIMARY KEY**: Cada linha tem uma ID única.
- **FOREIGN KEY**: Links entre tabelas (itens apontam para vendas).
- **CHECK**: Validações (valores não podem ser negativos, quantidade > 0).
- **SERIAL**: ID que cresce automaticamente.

Salve o arquivo como `0_criar_banco.sql`.

### 10.2 Criar o script Python `0_criar_banco.py`

Este arquivo executa o SQL acima:

**Conteúdo de `0_criar_banco.py`:**

```python
from banco import motor
from sqlalchemy import text, event

# Ler o arquivo SQL
with open('0_criar_banco.sql', 'r', encoding='utf-8') as arquivo:
    sql_content = arquivo.read()

# Conectar ao banco 'postgres' (padrão) para criar o novo banco
engine = motor('postgres')

if engine is None:
    print("❌ Falha ao conectar. Verifique suas credenciais no .env")
    exit(1)

print("✓ Conectado ao PostgreSQL")

# Ativar modo AUTOCOMMIT (necessário para CREATE DATABASE)
connection = engine.raw_connection()
connection.set_isolation_level(0)
cursor = connection.cursor()

try:
    # Encerrar conexões existentes
    cursor.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'cafeteria'
        AND pid <> pg_backend_pid()
    """)
    
    # Tentar dropar e criar o banco
    cursor.execute("DROP DATABASE IF EXISTS cafeteria")
    cursor.execute("CREATE DATABASE cafeteria ENCODING 'UTF8'")
    connection.commit()
    
    print("✓ Banco 'cafeteria' criado")
except Exception as e:
    print(f"❌ Erro ao criar banco: {e}")
    connection.rollback()
    exit(1)
finally:
    cursor.close()
    connection.close()

# Agora conectar ao novo banco e criar as tabelas
engine_cafeteria = motor('cafeteria')
connection = engine_cafeteria.connect()

try:
    # Executar cada comando SQL separadamente
    commands = sql_content.split(';')
    for cmd in commands:
        cmd = cmd.strip()
        if cmd and not cmd.startswith('--'):
            connection.execute(text(cmd))
    
    connection.commit()
    print("✓ Tabelas criadas com sucesso")
    
except Exception as e:
    print(f"❌ Erro ao criar tabelas: {e}")
    connection.rollback()
    exit(1)
finally:
    connection.close()

print("\n✅ Fase 0 concluída!")
```

Salve como `0_criar_banco.py`.

### 10.3 Executar a Fase 0

No terminal (com o ambiente virtual ativado):

```bash
python 0_criar_banco.py
```

Você deve ver:
```
✓ Conectado ao PostgreSQL
✓ Banco 'cafeteria' criado
✓ Tabelas criadas com sucesso

✅ Fase 0 concluída!
```

Se ver um erro de conexão, verifique:
1. PostgreSQL está rodando? (Teste com `psql --version`)
2. Credenciais corretas no `.env`?

---

## PARTE 11: FASE 1 - EXTRAIR DADOS PARA RAW

Esta fase lê os arquivos CSV e os insere nas tabelas `raw_vendas` e `raw_itens`.

### 11.1 Criar o script `1_extrair.py`

**Conteúdo de `1_extrair.py`:**

```python
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
```

**Explicação:**

- **`localizar_zip()`**: Verifica se os CSVs foram extraídos.
- **`carregar_csv()`**: Lê o CSV em pedaços (chunks) de 50 mil linhas, limpa a tabela e insere os dados.
- **Loop**: Processa cada arquivo no dicionário `ARQUIVOS` (do `config.py`).

Salve como `1_extrair.py`.

### 11.2 Executar a Fase 1

```bash
python 1_extrair.py
```

Você deve ver:
```
============================================================
FASE 1: EXTRAIR DADOS PARA RAW
============================================================

Carregando vendas.csv...
  → Limpando tabela raw_vendas...
  → Lendo data/vendas.csv...
    → 150 linhas inseridas...
✓ Tabela raw_vendas: 150 linhas carregadas

Carregando itens.csv...
  → Limpando tabela raw_itens...
  → Lendo data/itens.csv...
    → 491 linhas inseridas...
✓ Tabela raw_itens: 491 linhas carregadas

============================================================
✅ Fase 1 concluída com sucesso!
============================================================
```

---

## PARTE 12: FASE 2 - TRANSFORMAR PARA SILVER

Esta fase converte os dados brutos (texto) em dados tipados e limpos.

### 12.1 Entender as Conversões

Antes de rodar o script, vamos entender o que acontece:

**Conversão de Dinheiro:**
- **Entrada (texto):** "1.234,50" (formato brasileiro)
- **Saída (NUMERIC):** 1234.50 (número)
- **Processo:** Remove o ponto (separador de milhar), transforma a vírgula em ponto

**Conversão de Data:**
- **Entrada (texto):** "30/09/2025"
- **Saída (DATE):** 2025-09-30 (formato SQL)
- **Processo:** Reinterpreta o padrão DD/MM/YYYY

**Cálculos:**
- **valor_total:** valor_bruto - valor_desconto
- **prazo_dias:** data_entrega - data_pedido (diferença em dias)
- **subtotal (itens):** quantidade × preco_unitario

**Transação (Tudo ou Nada):**
Se qualquer passo falhar, todas as mudanças são desfeitas (rollback). Isso garante que o banco nunca fica "meio-transformado".

### 12.2 Criar o script `2_transformar.py`

**Conteúdo de `2_transformar.py`:**

```python
from banco import conectar, executar
from sqlalchemy.exc import SQLAlchemyError

print("=" * 60)
print("FASE 2: TRANSFORMAR DADOS PARA SILVER")
print("=" * 60 + "\n")

conexao = conectar('cafeteria')

if conexao is None:
    print("❌ Não foi possível conectar ao banco")
    exit(1)

try:
    print("→ Limpando tabelas silver (filha primeiro)...")
    executar(conexao, "DELETE FROM silver_itens", commit=False)
    executar(conexao, "DELETE FROM silver_vendas", commit=False)
    
    # ===== PASSO 1: INSERIR VENDAS =====
    print("→ Inserindo dados em silver_vendas...")
    sql_vendas = """
    INSERT INTO silver_vendas (
        id_venda, data_pedido, data_entrega, nome_loja, 
        id_cliente, valor_bruto, valor_desconto
    )
    SELECT
        CAST(TRIM(id_venda) AS INT),
        TO_DATE(TRIM(data_pedido), 'DD/MM/YYYY'),
        TO_DATE(TRIM(data_entrega), 'DD/MM/YYYY'),
        TRIM(nome_loja),
        CASE WHEN TRIM(id_cliente) = '' THEN NULL ELSE CAST(TRIM(id_cliente) AS INT) END,
        CASE WHEN TRIM(valor_bruto) = '' THEN NULL 
             ELSE CAST(REPLACE(REPLACE(TRIM(valor_bruto), '.', ''), ',', '.') AS NUMERIC(10,2)) END,
        CASE WHEN TRIM(valor_desconto) = '' THEN NULL 
             ELSE CAST(REPLACE(REPLACE(TRIM(valor_desconto), '.', ''), ',', '.') AS NUMERIC(10,2)) END
    FROM raw_vendas
    """
    executar(conexao, sql_vendas, commit=False)
    
    # ===== PASSO 2: CALCULAR valor_total E prazo_dias =====
    print("→ Calculando valor_total e prazo_dias...")
    sql_calc_vendas = """
    UPDATE silver_vendas SET
        valor_total = COALESCE(valor_bruto, 0) - COALESCE(valor_desconto, 0),
        prazo_dias = EXTRACT(DAY FROM data_entrega - data_pedido)::INT
    """
    executar(conexao, sql_calc_vendas, commit=False)
    
    # ===== PASSO 3: INSERIR ITENS =====
    print("→ Inserindo dados em silver_itens...")
    sql_itens = """
    INSERT INTO silver_itens (
        id_venda, sequencia_item, produto, categoria, 
        quantidade, preco_unitario
    )
    SELECT
        CAST(TRIM(ri.id_venda) AS INT),
        CAST(TRIM(ri.sequencia_item) AS INT),
        TRIM(ri.produto),
        TRIM(ri.categoria),
        CAST(TRIM(ri.quantidade) AS INT),
        CAST(REPLACE(REPLACE(TRIM(ri.preco_unitario), '.', ''), ',', '.') AS NUMERIC(10,2))
    FROM raw_itens ri
    WHERE TRIM(ri.id_venda) IN (SELECT id_venda::VARCHAR FROM silver_vendas)
    """
    executar(conexao, sql_itens, commit=False)
    
    # ===== PASSO 4: CALCULAR subtotal =====
    print("→ Calculando subtotal dos itens...")
    sql_calc_itens = """
    UPDATE silver_itens SET
        subtotal = quantidade * preco_unitario
    """
    executar(conexao, sql_calc_itens, commit=False)
    
    # ===== PASSO 5: COMMIT (CONFIRMA TUDO) =====
    print("→ Confirmando transação...")
    conexao.commit()
    
    print("\n✅ Fase 2 concluída com sucesso!")
    print("=" * 60)
    
except SQLAlchemyError as e:
    print(f"\n❌ Erro durante transformação: {e}")
    print("   Revertendo mudanças...")
    conexao.rollback()
    exit(1)
finally:
    conexao.close()
```

**Explicação de cada passo:**

1. **DELETE**: Limpa as tabelas silver para começar do zero
2. **INSERT INTO silver_vendas**: Converte tipos de dados (texto → INT, DATE, NUMERIC)
3. **UPDATE valor_total**: Calcula valor_bruto - valor_desconto
4. **INSERT INTO silver_itens**: Similar para itens
5. **UPDATE subtotal**: quantidade × preco_unitario
6. **commit()**: Se tudo funcionou, confirma. Se não, rollback() apaga tudo.

Salve como `2_transformar.py`.

### 12.3 Executar a Fase 2

```bash
python 2_transformar.py
```

Você deve ver:
```
============================================================
FASE 2: TRANSFORMAR DADOS PARA SILVER
============================================================

→ Limpando tabelas silver (filha primeiro)...
→ Inserindo dados em silver_vendas...
→ Calculando valor_total e prazo_dias...
→ Inserindo dados em silver_itens...
→ Calculando subtotal dos itens...
→ Confirmando transação...

✅ Fase 2 concluída com sucesso!
============================================================
```

---

## PARTE 13: FASE 3 - ANÁLISE (GOLD)

Esta fase responde perguntas de negócio usando os dados limpos.

### 13.1 Criar o notebook `3_analise.ipynb`

Um notebook é um arquivo que mistura código Python, resultados e explicações. Vamos criar um assim:

**No Terminal:**

```bash
jupyter notebook
```

Isso abre um navegador com a interface do Jupyter. Clique em "New" → "Python 3".

**Célula 1: Importar bibliotecas**

```python
import pandas as pd
from banco import conectar
import matplotlib.pyplot as plt

# Configuração de exibição
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
```

Pressione Shift+Enter para executar.

**Célula 2: Função auxiliar para consultas**

```python
def consultar(sql):
    """Executa uma query e retorna DataFrame."""
    conexao = conectar('cafeteria')
    if conexao is None:
        print("❌ Erro ao conectar")
        return None
    
    try:
        resultado = pd.read_sql(sql, conexao)
        conexao.close()
        return resultado
    except Exception as e:
        print(f"❌ Erro na query: {e}")
        conexao.close()
        return None

def reais(valor):
    """Formata um número como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
```

**Célula 3: P1 - Top 5 Lojas por Faturamento**

```python
print("=" * 60)
print("P1: RANKING DAS TOP 5 LOJAS POR FATURAMENTO")
print("=" * 60 + "\n")

sql_p1 = """
SELECT 
    nome_loja,
    ROUND(SUM(valor_total), 2) AS faturamento,
    COUNT(*) AS quantidade_vendas
FROM silver_vendas
GROUP BY nome_loja
ORDER BY faturamento DESC
LIMIT 5
"""

df_p1 = consultar(sql_p1)

if df_p1 is not None:
    df_p1['faturamento_formatado'] = df_p1['faturamento'].apply(reais)
    print(df_p1[['nome_loja', 'quantidade_vendas', 'faturamento_formatado']].to_string(index=False))
    print("\n")
```

**Célula 4: P2 - Top 3 Categorias**

```python
print("=" * 60)
print("P2: TOP 3 CATEGORIAS MAIS VENDIDAS")
print("=" * 60 + "\n")

sql_p2 = """
SELECT 
    categoria,
    COUNT(*) AS quantidade_itens,
    ROUND(SUM(subtotal), 2) AS faturamento
FROM silver_itens
GROUP BY categoria
ORDER BY faturamento DESC
LIMIT 3
"""

df_p2 = consultar(sql_p2)

if df_p2 is not None:
    df_p2['faturamento_formatado'] = df_p2['faturamento'].apply(reais)
    print(df_p2[['categoria', 'quantidade_itens', 'faturamento_formatado']].to_string(index=False))
    print("\n")
```

**Célula 5: P3 - Venda com Maior Prazo**

```python
print("=" * 60)
print("P3: VENDA COM MAIOR PRAZO DE ENTREGA")
print("=" * 60 + "\n")

sql_p3 = """
SELECT 
    id_venda,
    nome_loja,
    data_pedido,
    data_entrega,
    prazo_dias
FROM silver_vendas
ORDER BY prazo_dias DESC
LIMIT 1
"""

df_p3 = consultar(sql_p3)

if df_p3 is not None:
    venda = df_p3.iloc[0]
    print(f"ID da Venda: {venda['id_venda']}")
    print(f"Loja: {venda['nome_loja']}")
    print(f"Data do Pedido: {venda['data_pedido']}")
    print(f"Data de Entrega: {venda['data_entrega']}")
    print(f"Prazo: {venda['prazo_dias']} dias")
    print("\n")
```

**Célula 6: Criar Tabela Gold**

```python
print("=" * 60)
print("CRIANDO TABELA GOLD: RESUMO LOJA-CATEGORIA")
print("=" * 60 + "\n")

sql_gold = """
DROP TABLE IF EXISTS gold_loja_categoria;

CREATE TABLE gold_loja_categoria AS
SELECT
    sv.nome_loja,
    si.categoria,
    COUNT(DISTINCT si.id_venda) AS quantidade_vendas,
    COUNT(si.id_item) AS quantidade_itens,
    ROUND(SUM(si.subtotal), 2) AS faturamento
FROM silver_vendas sv
JOIN silver_itens si ON sv.id_venda = si.id_venda
GROUP BY sv.nome_loja, si.categoria
ORDER BY sv.nome_loja, faturamento DESC
"""

conexao = conectar('cafeteria')
if conexao:
    try:
        conexao.execute(sql_gold)
        conexao.commit()
        print("✓ Tabela gold_loja_categoria criada com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        conexao.rollback()
    finally:
        conexao.close()

# Mostrar preview
sql_preview = """
SELECT * FROM gold_loja_categoria LIMIT 10
"""

df_gold = consultar(sql_preview)
if df_gold is not None:
    print("\nPreview dos primeiros 10 registros:")
    print(df_gold.to_string(index=False))
    print("\n")
```

**Célula 7: Salvar o Notebook**

Clique em "File" → "Save As" e nomeie como `3_analise.ipynb`.

---

## PARTE 14: ENTENDER OS RESULTADOS

### 14.1 O que cada tabela contém

| Tabela | Conteúdo | Exemplo |
|--------|----------|---------|
| **raw_vendas** | Dados brutos do CSV (tudo texto) | id_venda="001", valor_bruto="1.234,50" |
| **raw_itens** | Itens brutos do CSV (tudo texto) | sequencia_item="1", quantidade="2" |
| **silver_vendas** | Vendas limpas e tipadas | id_venda=1 (INT), valor_bruto=1234.50 (NUMERIC) |
| **silver_itens** | Itens limpos e tipados | id_item=1 (auto), subtotal=50.00 (NUMERIC) |
| **gold_loja_categoria** | Resumo por loja e categoria | faturamento totalizados por loja e produto |

### 14.2 Fluxo dos dados

```
cafeteria.zip (CSVs)
        ↓
[FASE 1: Extrair]
        ↓
raw_vendas / raw_itens (texto puro)
        ↓
[FASE 2: Transformar]
        ↓
silver_vendas / silver_itens (dados limpos)
        ↓
[FASE 3: Analisar]
        ↓
gold_loja_categoria (resumos para negócio)
        ↓
Decisões e insights
```

---

## PARTE 15: VALIDAÇÃO E VERIFICAÇÃO

### 15.1 Conferir o Número de Linhas

Execute este código em uma célula Jupyter:

```python
sql_contagem = """
SELECT 
    'raw_vendas' AS tabela, COUNT(*) AS linhas FROM raw_vendas
UNION ALL
SELECT 'raw_itens', COUNT(*) FROM raw_itens
UNION ALL
SELECT 'silver_vendas', COUNT(*) FROM silver_vendas
UNION ALL
SELECT 'silver_itens', COUNT(*) FROM silver_itens
UNION ALL
SELECT 'gold_loja_categoria', COUNT(*) FROM gold_loja_categoria
"""

df_contagem = consultar(sql_contagem)
print(df_contagem.to_string(index=False))
```

Você deve ver:

| tabela | linhas |
|--------|--------|
| raw_vendas | 150 |
| raw_itens | 491 |
| silver_vendas | 150 |
| silver_itens | 491 |
| gold_loja_categoria | Vários |

### 15.2 Verificar Valores Nulos

```python
sql_nulls = """
SELECT 
    id_cliente,
    COUNT(*) AS quantidade
FROM silver_vendas
WHERE id_cliente IS NULL
GROUP BY id_cliente
"""

df_nulls = consultar(sql_nulls)
print(f"Vendas sem cliente: {len(df_nulls)}")
```

### 15.3 Conferir Conversões

```python
# Verificar se as datas foram convertidas corretamente
sql_datas = """
SELECT 
    MIN(data_pedido) AS primeira_data,
    MAX(data_entrega) AS ultima_data,
    MIN(prazo_dias) AS menor_prazo,
    MAX(prazo_dias) AS maior_prazo
FROM silver_vendas
"""

df_datas = consultar(sql_datas)
print(df_datas.to_string(index=False))
```

---

## PARTE 16: SOLUÇÃO DE PROBLEMAS

### Problema: "Erro ao conectar ao PostgreSQL"

**Causa:** Credenciais incorretas ou PostgreSQL não está rodando.

**Solução:**
1. Verifique se PostgreSQL está rodando:
   ```bash
   psql --version
   ```
2. Verifique as credenciais no `.env`:
   ```bash
   cat .env
   ```
3. Teste a conexão manualmente:
   ```bash
   psql -h localhost -U postgres -d postgres
   ```
   (Digite a senha que você criou)

### Problema: "ModuleNotFoundError: No module named 'pandas'"

**Causa:** Uma das bibliotecas não foi instalada.

**Solução:**
```bash
pip install pandas>=2.0 sqlalchemy>=2.0 psycopg2-binary>=2.9 matplotlib>=3.7 python-dotenv>=1.0 jupyter>=1.0
```

### Problema: "No such file or directory: 'data/cafeteria.zip'"

**Causa:** O arquivo ZIP não foi extraído.

**Solução:**
1. Verifique se o ZIP existe: `ls data/`
2. Extraia manualmente:
   ```bash
   unzip data/cafeteria.zip -d data/
   ```

### Problema: "UNIQUE violation on sequencia_item"

**Causa:** Dados duplicados no CSV.

**Solução:** Isso é normal e significa que o CSV tem duplicatas. O script `2_transformar.py` lida com isso via UNIQUE constraint.

### Problema: "relação (tabela) não existe"

**Causa:** As tabelas não foram criadas (Fase 0 falhou).

**Solução:**
```bash
python 0_criar_banco.py
```

---

## PARTE 17: PRÓXIMOS PASSOS

### 17.1 Personalizar as Análises

Você pode criar novas queries no notebook. Exemplo:

```python
# Qual categoria tem o maior ticket médio?
sql_ticket_medio = """
SELECT 
    categoria,
    ROUND(AVG(preco_unitario), 2) AS ticket_medio
FROM silver_itens
GROUP BY categoria
ORDER BY ticket_medio DESC
"""

df_ticket = consultar(sql_ticket_medio)
print(df_ticket.to_string(index=False))
```

### 17.2 Exportar Dados para Excel

```python
# Exportar a tabela gold para Excel
df_gold = consultar("SELECT * FROM gold_loja_categoria")
df_gold.to_excel('relatorio_loja_categoria.xlsx', index=False)
print("✓ Arquivo 'relatorio_loja_categoria.xlsx' criado")
```

### 17.3 Criar Gráficos

```python
import matplotlib.pyplot as plt

# Gráfico: Faturamento por Loja
sql_graf = """
SELECT nome_loja, SUM(valor_total) AS faturamento
FROM silver_vendas
GROUP BY nome_loja
ORDER BY faturamento DESC
"""

df_graf = consultar(sql_graf)

plt.figure(figsize=(10, 6))
plt.bar(df_graf['nome_loja'], df_graf['faturamento'])
plt.xlabel('Loja')
plt.ylabel('Faturamento (R$)')
plt.title('Faturamento por Loja')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

---

## Estrutura Final do Projeto

Seu projeto deve ficar assim:

```
cafeteria-pipeline/
├── .env                      (suas credenciais - NÃO compartilhe)
├── .gitignore                (contém .env para não commitar credenciais)
├── config.py                 (configurações do projeto)
├── banco.py                  (funções de banco de dados)
├── 0_criar_banco.sql         (DDL das tabelas)
├── 0_criar_banco.py          (executa o DDL)
├── 1_extrair.py              (fase 1: raw)
├── 2_transformar.py          (fase 2: silver)
├── 3_analise.ipynb           (fase 3: análise)
├── requirements.txt          (dependências Python)
├── data/
│   ├── cafeteria.zip         (dados originais)
│   ├── vendas.csv            (extraído do ZIP)
│   └── itens.csv             (extraído do ZIP)
└── venv/                     (ambiente virtual Python)
```

---

## Conclusão

Parabéns! Você acaba de executar um pipeline de dados completo:

✅ Configurou PostgreSQL e Python
✅ Criou um banco de dados relacional
✅ Carregou dados de CSVs
✅ Transformou dados brutos em dados limpos e tipados
✅ Realizou análises de negócio
✅ Validou resultados

Agora você entende como dados fluem de um arquivo bruto até se tornarem insights para decisões.

### Conceitos aprendidos:

- **Ambientes virtuais**: Isolação de dependências
- **Configuração**: Separação de credenciais via `.env`
- **Banco de dados relacional**: Estrutura, constraints, integridade
- **Transações**: Atomicidade ("tudo ou nada")
- **Pipeline ETL**: Extract → Transform → Load
- **Idempotência**: Scripts que podem rodar múltiplas vezes
- **Análise de dados**: SQL + Python para insights

Bom trabalho! 🚀
