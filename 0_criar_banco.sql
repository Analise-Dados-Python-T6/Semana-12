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