import mysql.connector
from mysql.connector import Error, pooling
import os

_DB_PARAMS = {
    'host':               'localhost',
    'user':               'root',
    'password':           '',
    'database':           'patafeliz',
    'charset':            'utf8mb4',
    'use_pure':           True,
    'connection_timeout': 10,
    'autocommit':         False,
}

_pool = None

def criar_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name='webapp_pool',
            pool_size=5,
            pool_reset_session=True,
            **_DB_PARAMS
        )

def get_connection():
    try:
        if _pool is None:
            criar_pool()
        return _pool.get_connection()
    except Error as e:
        raise Exception(f'Nao foi possivel obter conexao do pool: {e}')

def execute_query(sql, params=None, fetch=False):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
            return cursor.rowcount
    except Error as e:
        conn.rollback()
        raise Exception(f'Erro ao executar query: {e}')
    finally:
        cursor.close()
        conn.close()

def execute_one(sql, params=None):
    resultados = execute_query(sql, params, fetch=True)
    return resultados[0] if resultados else None

def iniciar_bd():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='')
        cursor = conn.cursor()
        sql_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(sql_path, 'r', encoding='utf-8') as f:
            script = f.read()
        for stmt in script.split(';'):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        cursor.close()
        conn.close()
        print('Banco e tabelas iniciados com sucesso.')
    except Exception as e:
        print(f'Erro ao iniciar banco: {e}')


def inserir_e_retornar_id(sql, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        raise Exception(f'Erro ao inserir: {e}')
    finally:
        cursor.close()
        conn.close()


def listar_funcoes():
    return execute_query('SELECT * FROM funcoes ORDER BY nome_funcao', fetch=True)

def buscar_funcao(id_funcao):
    return execute_one('SELECT * FROM funcoes WHERE id_funcao = %s', (id_funcao,))

def inserir_funcao(nome, descricao, status, perm_dashboard, perm_usuarios,
                   perm_funcoes, perm_pets, perm_servicos):
    sql = '''INSERT INTO funcoes (nome_funcao, descricao, status, perm_dashboard,
             perm_usuarios, perm_funcoes, perm_pets, perm_servicos)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    return inserir_e_retornar_id(sql, (nome, descricao, status, perm_dashboard,
                                       perm_usuarios, perm_funcoes, perm_pets, perm_servicos))

def atualizar_funcao(id_funcao, nome, descricao, status, perm_dashboard,
                     perm_usuarios, perm_funcoes, perm_pets, perm_servicos):
    sql = '''UPDATE funcoes SET nome_funcao=%s, descricao=%s, status=%s,
             perm_dashboard=%s, perm_usuarios=%s, perm_funcoes=%s,
             perm_pets=%s, perm_servicos=%s WHERE id_funcao=%s'''
    return execute_query(sql, (nome, descricao, status, perm_dashboard, perm_usuarios,
                               perm_funcoes, perm_pets, perm_servicos, id_funcao))

def excluir_funcao(id_funcao):
    return execute_query('DELETE FROM funcoes WHERE id_funcao = %s', (id_funcao,))


def listar_funcionarios():
    sql = '''SELECT f.id_funcionario, f.nome, f.email, f.tipo, f.ativo,
                    fn.nome_funcao
             FROM funcionarios f
             LEFT JOIN funcoes fn ON f.id_funcao = fn.id_funcao
             ORDER BY f.nome'''
    return execute_query(sql, fetch=True)

def buscar_funcionario(id_funcionario):
    return execute_one('SELECT * FROM funcionarios WHERE id_funcionario = %s',
                       (id_funcionario,))

def buscar_funcionario_por_email(email):
    return execute_one('SELECT * FROM funcionarios WHERE email = %s', (email,))

def inserir_funcionario(nome, email, senha, tipo, id_funcao):
    sql = '''INSERT INTO funcionarios (nome, email, senha, tipo, id_funcao)
             VALUES (%s, %s, %s, %s, %s)'''
    return inserir_e_retornar_id(sql, (nome, email, senha, tipo,
                                       id_funcao if id_funcao else None))

def atualizar_funcionario(id_funcionario, nome, email, tipo, id_funcao, ativo):
    sql = '''UPDATE funcionarios SET nome=%s, email=%s, tipo=%s,
             id_funcao=%s, ativo=%s WHERE id_funcionario=%s'''
    return execute_query(sql, (nome, email, tipo, id_funcao if id_funcao else None,
                               ativo, id_funcionario))

def atualizar_senha_funcionario(id_funcionario, nova_senha):
    return execute_query('UPDATE funcionarios SET senha=%s WHERE id_funcionario=%s',
                         (nova_senha, id_funcionario))

def excluir_funcionario(id_funcionario):
    return execute_query('DELETE FROM funcionarios WHERE id_funcionario = %s',
                         (id_funcionario,))


def listar_pets():
    return execute_query('SELECT * FROM pets ORDER BY nome', fetch=True)

def buscar_pet(id_pet):
    return execute_one('SELECT * FROM pets WHERE id_pet = %s', (id_pet,))

def inserir_pet(nome, especie, raca, tutor, idade, peso):
    sql = '''INSERT INTO pets (nome, especie, raca, tutor, idade, peso)
             VALUES (%s, %s, %s, %s, %s, %s)'''
    return inserir_e_retornar_id(sql, (nome, especie, raca, tutor, idade, peso))

def atualizar_pet(id_pet, nome, especie, raca, tutor, idade, peso):
    sql = '''UPDATE pets SET nome=%s, especie=%s, raca=%s, tutor=%s,
             idade=%s, peso=%s WHERE id_pet=%s'''
    return execute_query(sql, (nome, especie, raca, tutor, idade, peso, id_pet))

def excluir_pet(id_pet):
    return execute_query('DELETE FROM pets WHERE id_pet = %s', (id_pet,))


def listar_servicos():
    return execute_query('SELECT * FROM servicos ORDER BY nome', fetch=True)

def buscar_servico(id_servico):
    return execute_one('SELECT * FROM servicos WHERE id_servico = %s', (id_servico,))

def inserir_servico(nome, categoria, preco, duracao, disponivel):
    sql = '''INSERT INTO servicos (nome, categoria, preco, duracao, disponivel)
             VALUES (%s, %s, %s, %s, %s)'''
    return inserir_e_retornar_id(sql, (nome, categoria, preco, duracao, disponivel))

def atualizar_servico(id_servico, nome, categoria, preco, duracao, disponivel):
    sql = '''UPDATE servicos SET nome=%s, categoria=%s, preco=%s,
             duracao=%s, disponivel=%s WHERE id_servico=%s'''
    return execute_query(sql, (nome, categoria, preco, duracao, disponivel, id_servico))

def excluir_servico(id_servico):
    return execute_query('DELETE FROM servicos WHERE id_servico = %s', (id_servico,))
