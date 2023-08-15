from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from database import db
from models import Pergunta, Usuario, Sugestao
from utils import criptografar_senha, comparar_senhas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SECRET_KEY'] = 'equipi'

db.init_app(app)
with app.app_context():
    db.create_all()

# ========================= Código para configurar e gerenciar login =========================

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return Usuario.query.get(user_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

# ====================================== Rotas do Site =========================================

@app.route("/", methods=['GET', 'POST'])
def index():
    error = None

    if request.method == 'POST':
        user = request.form.get('usuario', False)
        user_password = request.form.get('senha', False)

        login = Usuario.query.filter_by(usuario=user).first()

        if login:
            if comparar_senhas(login.senha, user_password):
                login_user(login)
                return redirect('/menu')
            else:
                error = 'Usuário ou senha incorretos'
                return render_template('index.html', error=error)
        else:
            error = 'Usuário não cadastrado'
            return render_template('index.html', error=error)
    else:
        return render_template('index.html', error=error)
    

@app.route('/cadastro-usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    error = None

    if request.method == 'POST':
        user = request.form.get('usuario', False)
        user_password = criptografar_senha(request.form.get('senha', False))
        novo_usuario = Usuario(user, user_password)

        if Usuario.query.filter_by(usuario=user).first():
            error = 'Nome de usuário já existe'
            return render_template('casdastro-usuario.html', error=error)
        else:
            try:
                db.session.add(novo_usuario)
                db.session.commit()

                return redirect('/')
            except:
                error = 'Houve um erro ao cadastrar o usuario'
                return render_template('casdastro-usuario.html', error=error)
    else:
        return render_template('casdastro-usuario.html', error=error)


@app.route("/menu")
@login_required
def website_menu():
    return render_template('menu.html')


@app.route("/cadastro", methods=['GET', 'POST'])
@login_required
def cadastro():
    if request.method == 'POST':
        categoria = request.form.get('categorias', False)
        pergunta = request.form.get('pergunta', False)
        resposta = request.form.get('resposta', False)

        nova_pergunta = Pergunta(categoria=categoria, pergunta=pergunta, resposta=resposta)

        try:
            db.session.add(nova_pergunta)
            db.session.commit()
            return redirect('/cadastro')
        except:
            return 'Houve um erro ao tentar cadastrar a pergunta'
    else:
        return render_template('cadastro.html')


@app.route('/perguntas', methods=['GET', 'POST'])
@login_required
def perguntas():
    if request.method == 'POST':
        categoria = request.form.get('categorias', False)

        if categoria != "Geral":
            perguntas = Pergunta.query.filter_by(categoria=categoria).all()

            return render_template('perguntas.html', perguntas=perguntas)
        else:
            return redirect('/perguntas')
    else:
        perguntas = Pergunta.query.order_by(Pergunta.id).all()
        return render_template('perguntas.html', perguntas=perguntas)


@app.route('/atualiza/<int:id>', methods=['GET', 'POST'])
@login_required
def atualiza(id):
    pergunta = Pergunta.query.get_or_404(id)

    if request.method == 'POST':
        pergunta.categoria = request.form.get('categorias', False)
        pergunta.pergunta = request.form.get('pergunta', False)
        pergunta.resposta = request.form.get('resposta', False)

        try:
            db.session.commit()

            return redirect('/perguntas')
        except:
            return 'Ocorreu um problema ao tentar atualizar a pergunta'
    else:
        return render_template('atualiza.html', pergunta=pergunta)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    pergunta_to_delete = Pergunta.query.get_or_404(id)

    try:
        db.session.delete(pergunta_to_delete)
        db.session.commit()

        return redirect('/perguntas')
    except:
        return 'Ocorreu um problema ao tentar deletar a pergunta'


@app.route('/horarios-disciplinas')
@login_required
def horarios_disciplinas():
    return render_template('horarios-disciplinas.html')


# ================================== Rotas para acesso dos alunos =========================================

@app.route("/send", methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        categoria = request.form.get('categoria_aluno', False)
        pergunta = request.form.get('pergunta_aluno', False)

        sugestao = Sugestao(categoria=categoria, pergunta=pergunta)

        try:
            db.session.add(sugestao)
            db.session.commit()
            return redirect('/sucesso')
        except:
            return redirect('/erro')
    else:
        return redirect('/sugestao')

@app.route('/sugestao')
def sugestao():
    return render_template('sugestao.html')

@app.route('/sucesso')
def sucesso():
    return render_template('sugestaoenv.html')

@app.route('/erro')
def erro():
    return render_template('404.html')

@app.route('/index_aluno')
def index_aluno():
    return render_template('index_aluno.html')

@app.route('/sugestoes_enviadas')
def sugestoes_enviadas():
    return render_template('sugestoes_enviadas.html')

@app.route('/visualizar_sugestoes', methods=['GET', 'POST'])
def visualizar_sugestoes():
    categoria = request.form.get('categoria_sugestao', False)
    if request.method == 'POST':
        if categoria == "Geral":
            sugestao = Sugestao.query.order_by(Sugestao.id).all() 
        else:
            sugestao = Sugestao.query.filter_by(categoria=request.form.get('categoria_sugestao', False)).all()
    else:
        sugestao = Sugestao.query.order_by(Sugestao.id).all()
    return render_template('sugestoes_enviadas.html', sugestoes=sugestao)

    
@app.route('/delete_sugestao/<int:id>', methods=['GET', 'POST'])
def delete_sugestao(id):
    sugestao_to_delete = Sugestao.query.get_or_404(id)
    try:
        db.session.delete(sugestao_to_delete)
        db.session.commit()
        return redirect('/visualizar_sugestoes')
    except:
        return redirect('/erro')

@app.route('/adicionar_ao_banco/<int:id>', methods=['GET', 'POST'])
def adicionar_ao_banco(id):
    categoria = Sugestao.query.get_or_404(id).categoria
    pergunta = Sugestao.query.get_or_404(id).pergunta
    resposta = 'Clique em "Editar" para adicionar resposta'
    sugestao_to_delete = Sugestao.query.get_or_404(id)
    nova_pergunta = Pergunta(categoria=categoria, pergunta=pergunta, resposta=resposta)
    try:
        db.session.add(nova_pergunta)
        db.session.commit()
        db.session.delete(sugestao_to_delete)
        db.session.commit()
        return redirect('/perguntas')
    except:
        return redirect('/erro')

# ====================================== Redirecionamneto telegram =========================================

@app.route('/<pgEspecifica>', methods=['GET', 'POST'])
def respondeAi(pgEspecifica):
    if request.method == "GET":
        perguntas = Pergunta.query.all()
        for i in perguntas:
            if i.pergunta == (pgEspecifica + "?") or i.pergunta == pgEspecifica:
                return i.resposta
        return "Desculpe, sua dúvida não está em nosso banco de dado"

# ======================================== Execução do aplicativo =========================================
if __name__ == '__main__':
    app.run()