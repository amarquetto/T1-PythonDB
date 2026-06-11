-- DROP DATABASE patafeliz;

CREATE DATABASE IF NOT EXISTS patafeliz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE patafeliz;

CREATE TABLE IF NOT EXISTS funcoes (
    id_funcao     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome_funcao   VARCHAR(120) NOT NULL,
    descricao     TEXT,
    status        ENUM('ativo','inativo') DEFAULT 'ativo',
    perm_dashboard   BOOLEAN DEFAULT FALSE,
    perm_usuarios    BOOLEAN DEFAULT FALSE,
    perm_funcoes     BOOLEAN DEFAULT FALSE,
    perm_pets        BOOLEAN DEFAULT FALSE,
    perm_servicos    BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS funcionarios (
    id_funcionario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome           VARCHAR(255) NOT NULL,
    email          VARCHAR(255) UNIQUE NOT NULL,
    senha          VARCHAR(255) NOT NULL,
    tipo           ENUM('admin','veterinario','funcionario') DEFAULT 'funcionario',
    id_funcao      INT UNSIGNED,
    ativo          BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_funcao) REFERENCES funcoes(id_funcao) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS pets (
    id_pet   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome     VARCHAR(100) NOT NULL,
    especie  VARCHAR(50),
    raca     VARCHAR(100),
    tutor    VARCHAR(255),
    idade    INT,
    peso     VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS servicos (
    id_servico  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(255) NOT NULL,
    categoria   VARCHAR(100),
    preco       DECIMAL(10,2),
    duracao     VARCHAR(30),
    disponivel  ENUM('Sim','Nao') DEFAULT 'Sim'
);

INSERT IGNORE INTO funcionarios (id_funcionario, nome, email, senha, tipo)
VALUES 
    (1, 'Administrador', 'andre@gmail.com', '123456', 'admin'),
    (2, 'Administrador', 'ingrid@gmail.com', '123456', 'admin');
