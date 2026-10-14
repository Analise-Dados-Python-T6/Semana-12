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
