from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import db

app = Flask(__name__)
app.secret_key = 'patafeliz_secret_2024'

db.iniciar_bd()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'id' not in session:
            flash('Faça login para acessar.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('tipo') != 'admin':
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('listar_pets'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        usuario = db.execute_one('SELECT * FROM funcionarios WHERE email = %s', (email,))
        if usuario and usuario['senha'] == senha and usuario['ativo']:
            session['id'] = usuario['id_funcionario']
            session['nome'] = usuario['nome']
            session['tipo'] = usuario['tipo']
            flash(f'Bem-vindo, {usuario["nome"]}!', 'success')
            return redirect(url_for('listar_pets'))
        flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Voce saiu do sistema.', 'info')
    return redirect(url_for('login'))


# ─── FUNCOES ────────────────────────────────────────────────────

@app.route('/funcoes')
@login_required
@admin_required
def listar_funcoes():
    funcoes = db.execute_query('SELECT * FROM funcoes ORDER BY nome_funcao', fetch=True)
    return render_template('usuarios/listar_funcoes.html', funcoes=funcoes)


@app.route('/funcoes/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def inserir_funcao():
    if request.method == 'POST':
        nome = request.form.get('nome_funcao', '').strip()
        descricao = request.form.get('descricao_funcao', '').strip()
        status = request.form.get('status_funcao', 'ativo')
        perms = request.form.getlist('permissoes')
        if not nome:
            flash('Informe o nome da funcao.', 'danger')
        else:
            sql = '''INSERT INTO funcoes (nome_funcao, descricao, status, perm_dashboard,
                     perm_usuarios, perm_funcoes, perm_pets, perm_servicos)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            db.execute_query(sql, (
                nome, descricao, status,
                'dashboard' in perms,
                'usuarios' in perms,
                'funcoes' in perms,
                'pets' in perms,
                'servicos' in perms
            ))
            flash('Funcao cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_funcoes'))
    return render_template('usuarios/cadastrar_funcoes.html')


@app.route('/funcoes/editar/<int:id_funcao>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_funcao(id_funcao):
    funcao = db.execute_one('SELECT * FROM funcoes WHERE id_funcao = %s', (id_funcao,))
    if not funcao:
        flash('Funcao nao encontrada.', 'danger')
        return redirect(url_for('listar_funcoes'))
    if request.method == 'POST':
        nome = request.form.get('nome_funcao', '').strip()
        descricao = request.form.get('descricao_funcao', '').strip()
        status = request.form.get('status_funcao', 'ativo')
        perms = request.form.getlist('permissoes')
        if not nome:
            flash('Informe o nome da funcao.', 'danger')
        else:
            sql = '''UPDATE funcoes SET nome_funcao=%s, descricao=%s, status=%s,
                     perm_dashboard=%s, perm_usuarios=%s, perm_funcoes=%s,
                     perm_pets=%s, perm_servicos=%s WHERE id_funcao=%s'''
            db.execute_query(sql, (
                nome, descricao, status,
                'dashboard' in perms,
                'usuarios' in perms,
                'funcoes' in perms,
                'pets' in perms,
                'servicos' in perms,
                id_funcao
            ))
            flash('Funcao atualizada!', 'success')
            return redirect(url_for('listar_funcoes'))
    return render_template('usuarios/editar_funcao.html', funcao=funcao)


@app.route('/funcoes/excluir/<int:id_funcao>', methods=['POST'])
@login_required
@admin_required
def excluir_funcao(id_funcao):
    db.execute_query('DELETE FROM funcoes WHERE id_funcao = %s', (id_funcao,))
    flash('Funcao excluida.', 'success')
    return redirect(url_for('listar_funcoes'))


# ─── FUNCIONARIOS ───────────────────────────────────────────────

@app.route('/usuarios/listar')
@login_required
@admin_required
def listar_usuarios():
    sql = 'SELECT id_funcionario, nome, email, tipo, ativo FROM funcionarios ORDER BY nome'
    usuarios = db.execute_query(sql, fetch=True)
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)

@app.route('/usuarios/inserir', methods=['GET', 'POST'])
@login_required
@admin_required
def inserir_usuario():
    funcoes = db.execute_query('SELECT * FROM funcoes ORDER BY nome_funcao', fetch=True)
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        tipo = request.form.get('tipo', 'funcionario')
        id_funcao = request.form.get('id_funcao') or None
        if not nome or not email or not senha:
            flash('Preencha todos os campos obrigatorios.', 'danger')
        else:
            sql = '''INSERT INTO funcionarios (nome, email, senha, tipo, id_funcao)
                     VALUES (%s, %s, %s, %s, %s)'''
            db.execute_query(sql, (nome, email, senha, tipo, id_funcao))
            flash(f'Funcionario "{nome}" cadastrado!', 'success')
            return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/inserir_usuario.html', funcoes=funcoes)


@app.route('/usuarios/editar/<int:id_funcionario>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id_funcionario):
    usuario = db.execute_one('SELECT * FROM funcionarios WHERE id_funcionario = %s', (id_funcionario,))
    funcoes = db.execute_query('SELECT * FROM funcoes ORDER BY nome_funcao', fetch=True)
    if not usuario:
        flash('Funcionario nao encontrado.', 'danger')
        return redirect(url_for('listar_usuarios'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        tipo = request.form.get('tipo', 'funcionario')
        id_funcao = request.form.get('id_funcao') or None
        ativo = request.form.get('ativo', '1') == '1'
        nova_senha = request.form.get('senha', '').strip()
        if not nome or not email:
            flash('Preencha todos os campos.', 'danger')
        else:
            sql = '''UPDATE funcionarios SET nome=%s, email=%s, tipo=%s,
                     id_funcao=%s, ativo=%s WHERE id_funcionario=%s'''
            db.execute_query(sql, (nome, email, tipo, id_funcao, ativo, id_funcionario))
            if nova_senha:
                db.execute_query(
                    'UPDATE funcionarios SET senha=%s WHERE id_funcionario=%s',
                    (nova_senha, id_funcionario)
                )
            flash('Funcionario atualizado!', 'success')
            return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/editar_usuario.html', usuario=usuario, funcoes=funcoes)


@app.route('/usuarios/excluir/<int:id_funcionario>', methods=['POST'])
@login_required
@admin_required
def excluir_usuario(id_funcionario):
    if id_funcionario == session.get('id'):
        flash('Voce nao pode excluir sua propria conta.', 'danger')
    else:
        db.execute_query('DELETE FROM funcionarios WHERE id_funcionario = %s', (id_funcionario,))
        flash('Funcionario excluido.', 'success')
    return redirect(url_for('listar_usuarios'))


# ─── PETS ───────────────────────────────────────────────────────

@app.route('/pets/listar')
@login_required
def listar_pets():
    pets = db.execute_query('SELECT * FROM pets ORDER BY nome', fetch=True)
    return render_template('pets/listar_pets.html', pets=pets)


@app.route('/pets/inserir', methods=['GET', 'POST'])
@login_required
def inserir_pet():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        especie = request.form.get('especie', '').strip()
        raca = request.form.get('raca', '').strip() or 'SRD'
        tutor = request.form.get('tutor', '').strip()
        idade = request.form.get('idade', '0').strip()
        peso = request.form.get('peso', '').strip()
        if not nome or not especie or not tutor:
            flash('Preencha os campos obrigatorios.', 'danger')
        else:
            try:
                idade = int(idade)
            except ValueError:
                idade = 0
            sql = '''INSERT INTO pets (nome, especie, raca, tutor, idade, peso)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            db.execute_query(sql, (nome, especie, raca, tutor, idade, peso))
            flash(f'Pet "{nome}" cadastrado!', 'success')
            return redirect(url_for('listar_pets'))
    return render_template('pets/inserir_pet.html')


@app.route('/pets/editar/<int:id_pet>', methods=['GET', 'POST'])
@login_required
def editar_pet(id_pet):
    pet = db.execute_one('SELECT * FROM pets WHERE id_pet = %s', (id_pet,))
    if not pet:
        flash('Pet nao encontrado.', 'danger')
        return redirect(url_for('listar_pets'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        especie = request.form.get('especie', '').strip()
        raca = request.form.get('raca', '').strip() or 'SRD'
        tutor = request.form.get('tutor', '').strip()
        idade = request.form.get('idade', '0').strip()
        peso = request.form.get('peso', '').strip()
        if not nome or not especie or not tutor:
            flash('Preencha os campos obrigatorios.', 'danger')
        else:
            try:
                idade = int(idade)
            except ValueError:
                idade = 0
            sql = '''UPDATE pets SET nome=%s, especie=%s, raca=%s, tutor=%s,
                     idade=%s, peso=%s WHERE id_pet=%s'''
            db.execute_query(sql, (nome, especie, raca, tutor, idade, peso, id_pet))
            flash(f'Pet "{nome}" atualizado!', 'success')
            return redirect(url_for('listar_pets'))
    return render_template('pets/editar_pet.html', pet=pet)


@app.route('/pets/excluir/<int:id_pet>', methods=['POST'])
@login_required
def excluir_pet(id_pet):
    db.execute_query('DELETE FROM pets WHERE id_pet = %s', (id_pet,))
    flash('Pet excluido.', 'success')
    return redirect(url_for('listar_pets'))


# ─── SERVICOS ───────────────────────────────────────────────────

@app.route('/servicos/listar')
@login_required
def listar_servicos():
    servicos = db.execute_query('SELECT * FROM servicos ORDER BY nome', fetch=True)
    return render_template('servicos/listar_servicos.html', servicos=servicos)


@app.route('/servicos/inserir', methods=['GET', 'POST'])
@login_required
def inserir_servico():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', '').strip()
        preco = request.form.get('preco', '0').strip()
        duracao = request.form.get('duracao', '').strip()
        disponivel = request.form.get('disponivel', 'Sim')
        if not nome or not categoria or not preco:
            flash('Preencha os campos obrigatorios.', 'danger')
        else:
            try:
                preco = float(preco.replace(',', '.'))
            except ValueError:
                preco = 0.0
            sql = '''INSERT INTO servicos (nome, categoria, preco, duracao, disponivel)
                     VALUES (%s, %s, %s, %s, %s)'''
            db.execute_query(sql, (nome, categoria, preco, duracao, disponivel))
            flash(f'Servico "{nome}" cadastrado!', 'success')
            return redirect(url_for('listar_servicos'))
    return render_template('servicos/inserir_servico.html')


@app.route('/servicos/editar/<int:id_servico>', methods=['GET', 'POST'])
@login_required
def editar_servico(id_servico):
    servico = db.execute_one('SELECT * FROM servicos WHERE id_servico = %s', (id_servico,))
    if not servico:
        flash('Servico nao encontrado.', 'danger')
        return redirect(url_for('listar_servicos'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', '').strip()
        preco = request.form.get('preco', '0').strip()
        duracao = request.form.get('duracao', '').strip()
        disponivel = request.form.get('disponivel', 'Sim')
        if not nome or not categoria or not preco:
            flash('Preencha os campos obrigatorios.', 'danger')
        else:
            try:
                preco = float(preco.replace(',', '.'))
            except ValueError:
                preco = 0.0
            sql = '''UPDATE servicos SET nome=%s, categoria=%s, preco=%s,
                     duracao=%s, disponivel=%s WHERE id_servico=%s'''
            db.execute_query(sql, (nome, categoria, preco, duracao, disponivel, id_servico))
            flash(f'Servico "{nome}" atualizado!', 'success')
            return redirect(url_for('listar_servicos'))
    return render_template('servicos/editar_servico.html', servico=servico)


@app.route('/servicos/excluir/<int:id_servico>', methods=['POST'])
@login_required
def excluir_servico(id_servico):
    db.execute_query('DELETE FROM servicos WHERE id_servico = %s', (id_servico,))
    flash('Servico excluido.', 'success')
    return redirect(url_for('listar_servicos'))


@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')


if __name__ == '__main__':
    app.run(debug=True)