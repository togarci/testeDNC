from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from sqlalchemy import and_, or_, func
from src import db
import datetime, jwt

from src.model.Ponto import Ponto
from src.conttroller.controls.Authenticate import jwt_required
from src.conttroller.controls.ValidateFieldsRequest import ValidateFieldsRequest

validate = ValidateFieldsRequest()
bp = Blueprint('ponto', __name__, url_prefix='/ponto')

@bp.route('/cadastrar', methods=['POST'])
@jwt_required
def cadastrarPonto(current_user):
    try:
        dt = str(datetime.date.today())
        hr = str(datetime.datetime.now().time()).split('.')[0]

        list_today_ponto = Ponto.query.filter_by(data=dt, id_usuario=current_user.id).all()

        if len(list_today_ponto) % 2 == 0: tipo = 'E'
        else: tipo = 'S'

        ponto = Ponto(id_usuario=current_user.id, data=dt, hora=hr, tipo=tipo)
        db.session.add(ponto)
        db.session.commit()

        return jsonify({ "status": "ponto salvo com sucesso" }), 200

    except Exception as e:
        erro = { 'erro': f'{e}' }
        return jsonify(erro), 500

@bp.route('/adm/cadastrar', methods=['POST'])
@jwt_required
def cadastrarPontoAdm(current_user):
    if current_user.adm:
        validateFields = validate.validateAll([ 'id_usuario', 'data', 'hora', 'tipo' ], request)
        if not validateFields['status']:
            return jsonify({ "erro": validateFields['dataField'] }), 405

        try:
            ponto = Ponto(
                id_usuario=request.json['id_usuario'],
                data=request.json['data'],
                hora=request.json['hora'],
                tipo=request.json['tipo']
            )

            db.session.add(ponto)
            db.session.commit()

            return jsonify({ "status": "ponto salvo com sucesso" }), 200

        except Exception as e:
            erro = { 'erro': f'{e}' }
            return jsonify(erro), 500

@bp.route('/busca', methods=["GET"])
@jwt_required
def buscarTodosPonto(current_user):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", type=int)

    try:
        listPonto = Ponto.query.filter_by(id_usuario=current_user.id).paginate(page=page, per_page=per_page)

        data = []
        for ponto in listPonto.items:
            data.append({
                "data": ponto.data,
                "hora": ponto.hora,
                "tipo": ponto.tipo
            })

        return jsonify({ "count": len(data), "data": data }), 200

    except Exception as e:
        erro = { 'erro': f'{e}' }
        return jsonify(erro), 500

@bp.route('/busca/filtro', methods=["GET"])
@jwt_required
def buscaPontoFiltro(current_user):
    id_usuario = request.args.get("id_usuario")
    start_data = request.args.get("start_data")
    end_data = request.args.get("end_data")
    tipo = request.args.get("tipo")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", type=int)

    if current_user.adm:
        filter = and_()
        if id_usuario: filter.append(Ponto.id_usuario==id_usuario)
        if end_data: filter.append(Ponto.data<=end_data)
        if start_data: filter.append(Ponto.data>=start_data)
        if tipo: filter.append(Ponto.tipo==tipo)

        try:
            listPonto = Ponto.query.filter(filter).paginate(page=page, per_page=per_page)

            data = []
            for ponto in listPonto.items:
                data.append({
                    "data": ponto.data,
                    "hora": ponto.hora,
                    "tipo": ponto.tipo
                })

            return jsonify({ "count": len(data), "data": data }), 200

        except Exception as e:
            erro = { 'erro': f'{e}' }
            return jsonify(erro), 500
