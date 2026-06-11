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
        usuario = db.buscar_funcionario_por_email(email)
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
    funcoes = db.listar_funcoes()
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
            db.inserir_funcao(
                nome, descricao, status,
                'dashboard' in perms,
                'usuarios' in perms,
                'funcoes' in perms,
                'pets' in perms,
                'servicos' in perms
            )
            flash('Funcao cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_funcoes'))
    return render_template('usuarios/cadastrar_funcoes.html')


@app.route('/funcoes/editar/<int:id_funcao>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_funcao(id_funcao):
    funcao = db.buscar_funcao(id_funcao)
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
            db.atualizar_funcao(
                id_funcao, nome, descricao, status,
                'dashboard' in perms,
                'usuarios' in perms,
                'funcoes' in perms,
                'pets' in perms,
                'servicos' in perms
            )
            flash('Funcao atualizada!', 'success')
            return redirect(url_for('listar_funcoes'))
    return render_template('usuarios/editar_funcao.html', funcao=funcao)


@app.route('/funcoes/excluir/<int:id_funcao>', methods=['POST'])
@login_required
@admin_required
def excluir_funcao(id_funcao):
    db.excluir_funcao(id_funcao)
    flash('Funcao excluida.', 'success')
    return redirect(url_for('listar_funcoes'))


# ─── FUNCIONARIOS ───────────────────────────────────────────────

@app.route('/usuarios/listar')
@login_required
@admin_required
def listar_usuarios():
    usuarios = db.listar_funcionarios()
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)


@app.route('/usuarios/excluir-funcao/<int:funcao_id>', methods=['POST'])
@login_required
def excluir_funcao(funcao_id):
    """Remove uma função cadastrada pelo ID."""
    global funcoes
    funcao = next((f for f in funcoes if f['id'] == funcao_id), None)
    if funcao:
        funcoes = [f for f in funcoes if f['id'] != funcao_id]
        flash(f'Função "{funcao["nome"]}" excluída com sucesso!', 'success')
    else:
        flash('Função não encontrada.', 'danger')
    return redirect(url_for('listar_funcoes'))


@app.route('/usuarios/editar-funcao/<int:funcao_id>', methods=['GET', 'POST'])
@login_required
def editar_funcao(funcao_id):
    """
    GET  → exibe o formulário preenchido com os dados da função.
    POST → valida e atualiza a função em memória.
    """
    funcao = next((f for f in funcoes if f['id'] == funcao_id), None)
    if not funcao:
        flash('Função não encontrada.', 'danger')
        return redirect(url_for('listar_funcoes'))

    if request.method == 'POST':
        nome_funcao = request.form.get('nome_funcao', '').strip()
        status      = request.form.get('status_funcao', '').strip()
        descricao   = request.form.get('descricao_funcao', '').strip()
        permissoes  = request.form.getlist('permissoes')

        if not nome_funcao:
            flash('Informe o nome da função.', 'danger')
        elif len(nome_funcao) > 120:
            flash('O nome da função pode ter no máximo 120 caracteres.', 'danger')
        elif status not in ('ativo', 'inativo'):
            flash('Selecione se a função ficará ativa ou inativa.', 'danger')
        elif not descricao:
            flash('Informe a descrição com as responsabilidades da função.', 'danger')
        else:
            chaves_validas = {p['key'] for p in PERMISSOES_CATALOGO}
            funcao['nome']      = nome_funcao
            funcao['status']    = status
            funcao['descricao'] = descricao
            funcao['permissoes'] = [k for k in permissoes if k in chaves_validas]
            flash(f'Função "{nome_funcao}" atualizada com sucesso!', 'success')
            return redirect(url_for('listar_funcoes'))

    return render_template(
        'usuarios/editar_funcao.html',
        funcao=funcao,
        permissoes_catalogo=PERMISSOES_CATALOGO,
    )


@app.route('/usuarios/excluir/<int:usuario_id>', methods=['POST'])
@login_required
def excluir_usuario(usuario_id):
    """Remove um usuário pelo ID."""
    global usuarios
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    if usuario:
        usuarios = [u for u in usuarios if u['id'] != usuario_id]
        flash(f'Usuário "{usuario["nome"]}" excluído com sucesso!', 'success')
    else:
        flash('Usuário não encontrado.', 'danger')
    return redirect(url_for('listar_usuarios'))


@app.route('/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    """
    GET  → exibe o formulário preenchido com os dados do usuário.
    POST → valida e atualiza o usuário em memória.
    """
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('listar_usuarios'))

    if request.method == 'POST':
        nome   = request.form.get('nome', '').strip()
        email  = request.form.get('email', '').strip()
        perfil = request.form.get('perfil', '').strip()
        ativo  = request.form.get('ativo', '').strip()

        if not nome or not email or not perfil:
            flash('Preencha todos os campos obrigatórios.', 'danger')
        else:
            usuario['nome']   = nome
            usuario['email']  = email
            usuario['perfil'] = perfil
            usuario['ativo']  = ativo if ativo in ('Sim', 'Não') else 'Sim'
            flash(f'Usuário "{nome}" atualizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

    return render_template('usuarios/editar_usuario.html', usuario=usuario)


@app.route('/usuarios/inserir', methods=['GET', 'POST'])
@login_required
@admin_required
def inserir_usuario():
    funcoes = db.listar_funcoes()
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()
        tipo = request.form.get('tipo', 'funcionario')
        id_funcao = request.form.get('id_funcao') or None
        if not nome or not email or not senha:
            flash('Preencha todos os campos obrigatorios.', 'danger')
        else:
            db.inserir_funcionario(nome, email, senha, tipo, id_funcao)
            flash(f'Funcionario "{nome}" cadastrado!', 'success')
            return redirect(url_for('listar_usuarios'))
    return render_template('usuarios/inserir_usuario.html', funcoes=funcoes)


@app.route('/usuarios/editar/<int:id_funcionario>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id_funcionario):
    usuario = db.buscar_funcionario(id_funcionario)
    funcoes = db.listar_funcoes()
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
            db.atualizar_funcionario(id_funcionario, nome, email, tipo, id_funcao, ativo)
            if nova_senha:
                db.atualizar_senha_funcionario(id_funcionario, nova_senha)
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
        db.excluir_funcionario(id_funcionario)
        flash('Funcionario excluido.', 'success')
    return redirect(url_for('listar_usuarios'))


# ─── PETS ───────────────────────────────────────────────────────

@app.route('/pets/listar')
@login_required
def listar_pets():
    pets = db.listar_pets()
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
            db.inserir_pet(nome, especie, raca, tutor, idade, peso)
            flash(f'Pet "{nome}" cadastrado!', 'success')
            return redirect(url_for('listar_pets'))
    return render_template('pets/inserir_pet.html')


@app.route('/pets/editar/<int:id_pet>', methods=['GET', 'POST'])
@login_required
def editar_pet(id_pet):
    pet = db.buscar_pet(id_pet)
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
            db.atualizar_pet(id_pet, nome, especie, raca, tutor, idade, peso)
            flash(f'Pet "{nome}" atualizado!', 'success')
            return redirect(url_for('listar_pets'))
    return render_template('pets/editar_pet.html', pet=pet)


@app.route('/pets/excluir/<int:id_pet>', methods=['POST'])
@login_required
def excluir_pet(id_pet):
    db.excluir_pet(id_pet)
    flash('Pet excluido.', 'success')
    return redirect(url_for('listar_pets'))


# ─── SERVICOS ───────────────────────────────────────────────────

@app.route('/servicos/listar')
@login_required
def listar_servicos():
    servicos = db.listar_servicos()
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
            db.inserir_servico(nome, categoria, preco, duracao, disponivel)
            flash(f'Servico "{nome}" cadastrado!', 'success')
            return redirect(url_for('listar_servicos'))
    return render_template('servicos/inserir_servico.html')


@app.route('/servicos/editar/<int:id_servico>', methods=['GET', 'POST'])
@login_required
def editar_servico(id_servico):
    servico = db.buscar_servico(id_servico)
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
            db.atualizar_servico(id_servico, nome, categoria, preco, duracao, disponivel)
            flash(f'Servico "{nome}" atualizado!', 'success')
            return redirect(url_for('listar_servicos'))
    return render_template('servicos/editar_servico.html', servico=servico)


@app.route('/servicos/excluir/<int:id_servico>', methods=['POST'])
@login_required
def excluir_servico(id_servico):
    db.excluir_servico(id_servico)
    flash('Servico excluido.', 'success')
    return redirect(url_for('listar_servicos'))


@app.route('/equipe')
def equipe():
    return render_template('sobre_equipe.html')


if __name__ == '__main__':
    app.run(debug=True)
