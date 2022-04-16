from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from src import db
import datetime, jwt

from src.model.Usuario import Usuario
from src.conttroller.controls.Authenticate import jwt_required
from src.conttroller.controls.ValidateFieldsRequest import ValidateFieldsRequest

validate = ValidateFieldsRequest()
bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@bp.route('/cadastrar', methods=['POST'])
@jwt_required
def registerUser(current_user):
    if current_user.adm:
        validateFields = validate.validateAll([ 'nome', 'cpf', 'adm', 'senha' ], request)
        if not validateFields['status']:
            return jsonify({ "erro": validateFields['dataField'] }), 405

        try:
            usuario = Usuario(
                nome=request.json['nome'],
                cpf=request.json['cpf'],
                adm=request.json['adm'],
                senha=request.json['senha']
            )

            db.session.add(usuario)
            db.session.commit()

            payload = {
                "id": usuario.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }

            token = jwt.encode(payload, current_app.config['SECRET_KEY'])

            data = { "id_usuario": f'{usuario.id}', "status": "cadastro efetuado com sucesso", "token": f'{token.decode("utf-8")}' }

            return jsonify(data)


        except Exception as e:
            erro = { 'erro': f'{e}' }
            return jsonify(erro), 500
    else:
        return jsonify({"Erro": "voce nao pussui acesso para realizar esta transacao"})


@bp.route('/entrar', methods=['POST'])
def login():
    validateFields = validate.validateAll([ 'cpf', 'senha' ], request)
    if not validateFields['status']:
        return Response('{"Error": %r }' % validateFields['dataField'], mimetype="application/json", status=405)

    try:
        cpf = request.json['cpf']
        senha = request.json['senha']

        usuario = Usuario.query.filter_by(cpf=cpf).first()
        if usuario:
            if not usuario.verify_password(senha):
                return jsonify({ "error": "Senha incorreta" }), 403

            payload = {
                "id": usuario.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=15)
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'])

            return jsonify({ "id_user": usuario.id, "adm": usuario.adm, "token": f'{token.decode("utf-8") }', "status": "LogIn Efetuado" })
        else:
            return jsonify({ "erro": "Colaborador nao cadastrado "}), 404

    except Exception as e:
        erro = { 'erro': f'{e}' }
        return jsonify({ "erro": erro })
