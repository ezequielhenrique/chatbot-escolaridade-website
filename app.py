from flask import Flask, render_template, request, redirect
from database import db
from models import Pergunta
from flask_mail import Mail, Message
from config import email, senha, key
import ssl
import smtplib

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)
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

        print(categoria, pergunta, resposta)
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
    print(id)

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


@app.route("/index_aluno")
def index_aluno():
    return render_template('index_aluno.html')

@app.route("/sugestao")
def sugestao():
    return render_template('sugestao.html')

#______     INICIALIZANDO O FLASK-MAIL     ______

mail_settings = {
    "MAIL_SERVER" : 'smtp.gmail.com',
    "MAIL_PORT" : 587,
    "MAIL_USE_TLS" : True,
    "MAIL_USE_SSL" : True,
    "MAIL_USERNAME" : email,
    "MAIL_PASSWORD" : senha,
    "SECRET_KEY" : key
}

mail = Mail(app)

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        categoria = request.form.get('categoria_aluno')
        pergunta = request.form.get('pergunta_aluno')
        subject = 'Nova sugestão de pergunta'
        msg = Message(
                subject=subject,                                                          
                sender=email, 
                recipients=['escolaridadeuabj@gmail.com'],
                body=f'''
                Categoria - {categoria}
                Pergunta - {pergunta}
                
            '''   )
        try:
            mail.send(msg)
            return redirect('/sucesso')
        except:
            return redirect('/erro')


#________________________________________________________

@app.route('/sucesso')
def sucesso():
    return render_template('sugestaoenv.html')

@app.route('/erro')
def erro():
    return render_template('404.html')








if __name__ == '__main__':
    app.run(debug=True)