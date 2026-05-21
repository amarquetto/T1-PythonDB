-- ============================================
-- BANCO DE DADOS PATAFELIZ - PETSHOP
-- Sistema de Gerenciamento Completo
-- ============================================

-- DROP DATABASE IF EXISTS patafeliz;

CREATE DATABASE patafeliz;

USE patafeliz;

-- ============================================
-- TABELA: USUARIOS
-- Armazena dados dos usuários do sistema
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: CLIENTES
-- Informações complementares dos clientes
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: CATEGORIAS
-- Categorias de produtos e serviços
-- ============================================
CREATE TABLE IF NOT EXISTS categorias(
    id_categoria BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo ENUM('produto', 'servico') NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: PRODUTOS
-- Produtos disponíveis no petshop
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: ANIMAIS
-- Pets dos clientes
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: SERVICOS
-- Serviços oferecidos (banho, tosa, consulta, etc)
-- ============================================
CREATE TABLE IF NOT EXISTS servicos(
    id_servico BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_servico VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    duracao_minutos INT,
    id_categoria BIGINT UNSIGNED,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: AGENDAMENTOS
-- Agendamentos de serviços
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: VENDAS
-- Registro de vendas realizadas
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: ITENS_VENDA
-- Itens (produtos) de cada venda
-- ============================================
CREATE TABLE IF NOT EXISTS itens_venda(
    id_item_venda BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_venda BIGINT UNSIGNED NOT NULL,
    id_produto BIGINT UNSIGNED NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES vendas(id_venda) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: HISTORICO_MEDICO
-- Histórico médico dos animais
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: VACINAS
-- Controle de vacinação dos animais
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: FORNECEDORES
-- Fornecedores de produtos
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: COMPRAS
-- Registro de compras de fornecedores
-- ============================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TABELA: ITENS_COMPRA
-- Itens (produtos) de cada compra
-- ============================================
CREATE TABLE IF NOT EXISTS itens_compra(
    id_item_compra BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_compra BIGINT UNSIGNED NOT NULL,
    id_produto BIGINT UNSIGNED NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- ÍNDICES PARA MELHOR PERFORMANCE
-- ============================================

-- Índices para busca rápida
CREATE INDEX idx_usuarios_cpf ON usuarios(cpf);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_produtos_nome ON produtos(nome);
CREATE INDEX idx_vendas_data ON vendas(data_venda);
CREATE INDEX idx_agendamentos_data ON agendamentos(data_agendamento);
CREATE INDEX idx_animais_cliente ON animais(id_cliente);

-- ============================================
-- DADOS INICIAIS (SEED)
-- ============================================

-- Inserir categorias padrão de produtos
INSERT INTO categorias (nome_categoria, descricao, tipo) VALUES
('Rações', 'Alimentos para animais', 'produto'),
('Brinquedos', 'Brinquedos e acessórios para diversão', 'produto'),
('Higiene', 'Produtos de higiene e limpeza', 'produto'),
('Acessórios', 'Coleiras, guias e acessórios', 'produto'),
('Medicamentos', 'Medicamentos e suplementos', 'produto');

-- Inserir categorias padrão de serviços
INSERT INTO categorias (nome_categoria, descricao, tipo) VALUES
('Banho e Tosa', 'Serviços de banho e tosa', 'servico'),
('Veterinária', 'Consultas e procedimentos veterinários', 'servico'),
('Hotel', 'Hospedagem de animais', 'servico'),
('Adestramento', 'Treinamento e adestramento', 'servico');

-- Inserir usuário administrador padrão (senha: admin123)
INSERT INTO usuarios (nome, cpf, email, telefone, senha, tipo_usuario) VALUES
('Administrador', '000.000.000-00', 'admin@patafeliz.com', '(19) 99999-9999', 
 '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin');

-- ============================================
-- VIEWS ÚTEIS
-- ============================================

-- View: Produtos com estoque baixo
CREATE VIEW vw_produtos_estoque_baixo AS
SELECT 
    p.id_produto,
    p.nome,
    p.quantidade_estoque,
    p.estoque_minimo,
    c.nome_categoria,
    (p.estoque_minimo - p.quantidade_estoque) AS quantidade_repor
FROM produtos p
LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
WHERE p.quantidade_estoque < p.estoque_minimo
AND p.ativo = TRUE;

-- View: Agendamentos do dia
CREATE VIEW vw_agendamentos_hoje AS
SELECT 
    a.id_agendamento,
    a.data_agendamento,
    a.hora_inicio,
    a.hora_fim,
    a.status,
    u.nome AS nome_cliente,
    an.nome_animal,
    an.especie,
    s.nome_servico,
    a.valor
FROM agendamentos a
INNER JOIN clientes c ON a.id_cliente = c.id_cliente
INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
INNER JOIN animais an ON a.id_animal = an.id_animal
INNER JOIN servicos s ON a.id_servico = s.id_servico
WHERE a.data_agendamento = CURDATE()
ORDER BY a.hora_inicio;

-- View: Relatório de vendas
CREATE VIEW vw_relatorio_vendas AS
SELECT 
    v.id_venda,
    v.data_venda,
    u.nome AS vendedor,
    c.nome AS cliente,
    v.valor_total,
    v.desconto,
    v.valor_final,
    v.forma_pagamento,
    v.status,
    COUNT(iv.id_item_venda) AS total_itens
FROM vendas v
INNER JOIN usuarios u ON v.id_usuario = u.id_usuario
LEFT JOIN clientes cl ON v.id_cliente = cl.id_cliente
LEFT JOIN usuarios c ON cl.id_usuario = c.id_usuario
LEFT JOIN itens_venda iv ON v.id_venda = iv.id_venda
GROUP BY v.id_venda;

-- ============================================
-- TRIGGERS
-- ============================================

-- Trigger: Atualizar estoque após venda
DELIMITER $$
CREATE TRIGGER trg_atualizar_estoque_venda
AFTER INSERT ON itens_venda
FOR EACH ROW
BEGIN
    UPDATE produtos 
    SET quantidade_estoque = quantidade_estoque - NEW.quantidade
    WHERE id_produto = NEW.id_produto;
END$$
DELIMITER ;

-- Trigger: Calcular subtotal do item de venda
DELIMITER $$
CREATE TRIGGER trg_calcular_subtotal_venda
BEFORE INSERT ON itens_venda
FOR EACH ROW
BEGIN
    SET NEW.subtotal = NEW.quantidade * NEW.preco_unitario;
END$$
DELIMITER ;

-- Trigger: Calcular subtotal do item de compra
DELIMITER $$
CREATE TRIGGER trg_calcular_subtotal_compra
BEFORE INSERT ON itens_compra
FOR EACH ROW
BEGIN
    SET NEW.subtotal = NEW.quantidade * NEW.preco_unitario;
END$$
DELIMITER ;

-- Trigger: Atualizar estoque após compra recebida
DELIMITER $$
CREATE TRIGGER trg_atualizar_estoque_compra
AFTER UPDATE ON compras
FOR EACH ROW
BEGIN
    IF NEW.status = 'recebido' AND OLD.status != 'recebido' THEN
        UPDATE produtos p
        INNER JOIN itens_compra ic ON p.id_produto = ic.id_produto
        SET p.quantidade_estoque = p.quantidade_estoque + ic.quantidade
        WHERE ic.id_compra = NEW.id_compra;
    END IF;
END$$
DELIMITER ;

-- Verificar tabelas criadas
SHOW TABLES;