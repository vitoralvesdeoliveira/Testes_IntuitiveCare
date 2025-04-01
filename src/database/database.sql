-- Criar tabelas
CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    data_registro_ans DATE,
);

CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    data DATE,
    conta VARCHAR(100),
    descricao VARCHAR(255),
    valor DECIMAL(15,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- Importar dados (PostgreSQL)
COPY operadoras FROM '/caminho/para/operadoras_ativas.csv' DELIMITER ',' CSV HEADER ENCODING 'UTF8';

-- Query 1: Top 10 operadoras com maiores despesas no último trimestre
SELECT o.razao_social, o.nome_fantasia, SUM(d.valor) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
AND d.data >= DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '3 months'
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;

-- Query 2: Top 10 operadoras com maiores despesas no último ano
SELECT o.razao_social, o.nome_fantasia, SUM(d.valor) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
AND d.data >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;