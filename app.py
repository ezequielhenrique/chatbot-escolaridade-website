from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# cria uma instância do aplicativo
app = Flask(__name__)
# configura um banco de dados SQLite para o aplicativo
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# cria uma instância do banco de dados
db = SQLAlchemy()

# classes que irão definir as tabelas do banco de dados
class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(200), nullable=False)
    pergunta = db.Column(db.String(200), nullable=False)
    resposta = db.Column(db.String(200), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)


# inicializa o banco de dados
db.init_app(app)
# adciona as tabelas ao banco de dados
with app.app_context():
    db.create_all()

#  ----- rotas do site -----

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form.get('usuario', False)
        user_password = request.form.get('senha', False)

        if user != None and user_password != None:
            return render_template('menu.html')
    else:
        return render_template('index.html')


@app.route("/menu")
def website_menu():
    return render_template('menu.html')


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    print(request.method)
    if request.method == 'POST':
        categoria = request.form.get('categorias', False)
        pergunta = request.form.get('pergunta', False)
        resposta = request.form.get('resposta', False)

        nova_pergunta = Pergunta(categoria=categoria, pergunta=pergunta, resposta=resposta)

        try:
            db.session.add(nova_pergunta)
            db.session.commit()
            return redirect('/menu')
        except:
            return 'Houve um erro ao tentar cadastrar a pergunta'
    else:
        return render_template('cadastro.html')


@app.route('/perguntas', methods=['GET', 'POST'])
def perguntas():
    if request.method == 'POST':
        return render_template('menu.html')
    else:
        perguntas = Pergunta.query.order_by(Pergunta.id).all()
        return render_template('perguntas.html', perguntas=perguntas)


@app.route('/delete/<int:id>')      # Rota para deletar as perguntas (Não é uma página)
def delete(id):
    pergunta_to_delete = Pergunta.query.get_or_404(id)

    try:
        db.session.delete(pergunta_to_delete)
        db.session.commit()

        return redirect('/perguntas')
    except:
        return 'Ocorreu um problema ao tentar deletar a tarefa'
