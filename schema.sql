-- BANCO DE DADOS PATAFELIZ - PETSHOP

DROP DATABASE IF EXISTS patafeliz;

CREATE DATABASE IF NOT EXISTS patafeliz
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE patafeliz;


CREATE TABLE IF NOT EXISTS usuarios(
    id_usuario BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    senha VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('admin', 'funcionario', 'cliente') DEFAULT 'cliente',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS clientes(
    id_cliente BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario BIGINT UNSIGNED NOT NULL,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    data_nascimento DATE,
    observacoes TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS categorias(
    id_categoria BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo ENUM('produto', 'servico') NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS produtos(
    id_produto BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade_estoque INT DEFAULT 0,
    id_categoria BIGINT UNSIGNED,
    estoque_minimo INT DEFAULT 10,
    codigo_barras VARCHAR(50),
    marca VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS animais(
    id_animal BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente BIGINT UNSIGNED NOT NULL,
    nome_animal VARCHAR(100) NOT NULL,
    especie ENUM('cachorro', 'gato', 'passaro', 'roedor', 'reptil', 'outro') NOT NULL,
    raca VARCHAR(100),
    data_nascimento DATE,
    peso DECIMAL(5, 2),
    sexo ENUM('macho', 'femea'),
    cor VARCHAR(50),
    observacoes TEXT,
    foto VARCHAR(255),
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS servicos(
    id_servico BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_servico VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    duracao_minutos INT,
    id_categoria BIGINT UNSIGNED,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS agendamentos(
    id_agendamento BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente BIGINT UNSIGNED NOT NULL,
    id_animal BIGINT UNSIGNED NOT NULL,
    id_servico BIGINT UNSIGNED NOT NULL,
    data_agendamento DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME,
    status ENUM('agendado', 'confirmado', 'em_atendimento', 'concluido', 'cancelado') DEFAULT 'agendado',
    observacoes TEXT,
    valor DECIMAL(10, 2),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_animal) REFERENCES animais(id_animal) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servicos(id_servico) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vendas(
    id_venda BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_cliente BIGINT UNSIGNED,
    id_usuario BIGINT UNSIGNED NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10, 2) NOT NULL,
    desconto DECIMAL(10, 2) DEFAULT 0.00,
    valor_final DECIMAL(10, 2) NOT NULL,
    forma_pagamento ENUM('dinheiro', 'cartao_credito', 'cartao_debito', 'pix', 'boleto') NOT NULL,
    status ENUM('pendente', 'pago', 'cancelado') DEFAULT 'pago',
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS itens_venda(
    id_item_venda BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_venda BIGINT UNSIGNED NOT NULL,
    id_produto BIGINT UNSIGNED NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES vendas(id_venda) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS historico_medico(
    id_historico BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_animal BIGINT UNSIGNED NOT NULL,
    data_atendimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_atendimento VARCHAR(100),
    descricao TEXT,
    veterinario VARCHAR(255),
    medicamentos TEXT,
    proxima_consulta DATE,
    FOREIGN KEY (id_animal) REFERENCES animais(id_animal) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vacinas(
    id_vacina BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_animal BIGINT UNSIGNED NOT NULL,
    nome_vacina VARCHAR(100) NOT NULL,
    data_aplicacao DATE NOT NULL,
    data_proxima_dose DATE,
    lote VARCHAR(50),
    veterinario VARCHAR(255),
    observacoes TEXT,
    FOREIGN KEY (id_animal) REFERENCES animais(id_animal) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fornecedores(
    id_fornecedor BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_fornecedor VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(255),
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS compras(
    id_compra BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_fornecedor BIGINT UNSIGNED NOT NULL,
    id_usuario BIGINT UNSIGNED NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10, 2) NOT NULL,
    status ENUM('pendente', 'recebido', 'cancelado') DEFAULT 'pendente',
    nota_fiscal VARCHAR(100),
    observacoes TEXT,
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS itens_compra(
    id_item_compra BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_compra BIGINT UNSIGNED NOT NULL,
    id_produto BIGINT UNSIGNED NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE
);

-- DADOS INICIAIS 
INSERT INTO categorias (nome_categoria, descricao, tipo) VALUES
('Rações', 'Alimentos para animais', 'produto'),
('Brinquedos', 'Brinquedos e acessórios para diversão', 'produto'),
('Higiene', 'Produtos de higiene e limpeza', 'produto'),
('Acessórios', 'Coleiras, guias e acessórios', 'produto'),
('Medicamentos', 'Medicamentos e suplementos', 'produto');

INSERT INTO categorias (nome_categoria, descricao, tipo) VALUES
('Banho e Tosa', 'Serviços de banho e tosa', 'servico'),
('Veterinária', 'Consultas e procedimentos veterinários', 'servico'),
('Hotel', 'Hospedagem de animais', 'servico'),
('Adestramento', 'Treinamento e adestramento', 'servico');