from flask import Flask, render_template, request, redirect, flash
from database import db
from models import Pergunta, Usuario
from utils import criptografar_senha, comparar_senhas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)
with app.app_context():
    db.create_all()

#  ----- rotas do site -----

@app.route("/", methods=['GET', 'POST'])
def index():
    error = None

    if request.method == 'POST':
        user = request.form.get('usuario', False)
        user_password = request.form.get('senha', False)

        login = Usuario.query.filter_by(usuario=user).first()

        if login:
            if comparar_senhas(login.senha, user_password):
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
def website_menu():
    return render_template('menu.html')


@app.route("/cadastro", methods=['GET', 'POST'])
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
def delete(id):
    pergunta_to_delete = Pergunta.query.get_or_404(id)

    try:
        db.session.delete(pergunta_to_delete)
        db.session.commit()

        return redirect('/perguntas')
    except:
        return 'Ocorreu um problema ao tentar deletar a pergunta'
    

#________________________________ INICIALIZAÇÃO DA INTEGRAÇÃO DO SITE DO ALUNO ____________________________________

@app.route('/sucesso')
def sucesso():
    return render_template('sugestaoenv.html')

@app.route('/erro')
def erro():
    return render_template('404.html')


#____________________________ FLASK RUN ________________________
if __name__ == '__main__':
    app.run()