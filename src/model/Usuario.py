from werkzeug.security import generate_password_hash, check_password_hash
from src import db
import json

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    adm = db.Column(db.Boolean, default=False)
    senha = db.Column(db.String, nullable=False)


    def __init__(self, nome, cpf, adm, senha):
        self.nome = nome
        self.cpf = cpf
        self.adm = adm
        self.senha = generate_password_hash(senha)

    def verify_password(self, senha):
        return check_password_hash(self.senha, senha)

    def __repr__(self):
        return json.dumps({ 'id': self.id, 'nome': self.nome, 'cpf': self.cpf, 'adm': self.adm })
