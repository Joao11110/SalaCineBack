from flask import Blueprint, request, jsonify
from datetime import datetime
from Controller.SessaoController import SessaoController

sessao_bp = Blueprint('sessao', __name__)

@sessao_bp.route('/sessoes', methods=['POST'])
def cadastrar_sessao():
    data = request.get_json()
    try:
        data_hora = datetime.fromisoformat(data['data_hora'])
    except (ValueError, KeyError):
        return jsonify({'error': 'Formato de data/hora inválido'}), 400

    sessao = SessaoController.agendar(
        id_filme=data['id_filme'],
        id_sala=data['id_sala'],
        data_hora=data_hora
    )

    if not sessao:
        return jsonify({'error': 'Não foi possível agendar a sessão'}), 400

    return jsonify({
        'message': 'Sessão cadastrada com sucesso',
        'sessao': {
            'id_sessao': sessao.get_id_sessao(),
            'data_hora': sessao.data_hora.isoformat(),
            'filme': {
                'id_filme': sessao.filme.get_id_filme(),
                'titulo': sessao.filme.titulo
            },
            'sala': {
                'id_sala': sessao.sala.get_id_sala(),
                'numero_sala': sessao.sala.numero_sala
            }
        }
    }), 201

# @sessao_bp.route('/sessoes', methods=['GET'])
# def listar_sessoes():
#     data_str = request.args.get('data')
#     data = datetime.fromisoformat(data_str) if data_str else None
#     sessoes = SessaoController.listar_por_data(data)

#     return jsonify([{
#         'id_sessao': s.get_id_sessao(),
#         'data_hora': s.data_hora.isoformat(),
#         'filme': {
#             'id_filme': s.filme.get_id_filme(),
#             'titulo': s.filme.titulo
#         },
#         'sala': {
#             'id_sala': s.sala.get_id_sala(),
#             'numero_sala': s.sala.numero_sala
#         }
#     } for s in sessoes]), 200