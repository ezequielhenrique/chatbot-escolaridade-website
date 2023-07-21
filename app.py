from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('menu.html')
    else:
        return render_template('index.html')


@app.route("/menu")
def website_menu():
    return render_template('menu.html')


@app.route("/menu/cadastro")
@app.route("/cadastro")
def menu():
<<<<<<< Updated upstream
    return render_template('cadastro.html')
=======
    if request.method == 'POST':
        return render_template('menu.html')
    else:
        return render_template('cadastro.html')


@app.route('/perguntas')
def perguntas():
    return render_template('perguntas.html')
>>>>>>> Stashed changes
