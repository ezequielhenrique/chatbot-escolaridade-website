from database import db


class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    pergunta = db.Column(db.String(200), nullable=False)
    resposta = db.Column(db.String(400), nullable=False)

    def __init__(self, categoria, pergunta, resposta):
        self.categoria = categoria
        self.pergunta = pergunta
        self.resposta = resposta


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(64), nullable=False)

    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha

    def __repr__(self):
        return f'<Usuario {self.usuario}>'