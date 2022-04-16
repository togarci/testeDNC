from src import db
from src.model.Usuario import Usuario
from datetime import datetime, date
import json


class Ponto(db.Model):
    __tablename__= 'ponto'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    tipo = db.Column(db.String(1), nullable=False)

    def __init__(self, id_usuario, data, hora, tipo):
        self.id_usuario = id_usuario
        self.data = data
        self.hora = hora
        self.tipo = tipo

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'id_usuario': self.id_usuario,
            'data': self.data,
            'hora': self.hora,
            'tipo': self.tipo
        })
