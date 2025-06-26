from flask import Blueprint, request, jsonify
from Controller.SalaController import SalaController

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['POST'])
def cadastrar_sala():
    data = request.get_json()
    sala = SalaController.cadastrar(
        numero_sala=data['numero_sala'],
        local=data['local'],
        classificacao=data['classificacao']
    )
    return jsonify({'id_sala': sala.get_id_sala()}), 201

# @sala_bp.route('/salas/<int:id_sala>', methods=['PUT'])
# def editar_sala(id_sala):
#     data = request.get_json()
#     updated = SalaController.editar(id_sala, **data)
#     return jsonify({'updated': updated}), 200

# @sala_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
# def excluir_sala(id_sala):
#     deleted = SalaController.excluir(id_sala)
#     return jsonify({'deleted': deleted}), 200

# @sala_bp.route('/salas/<int:numero_sala>', methods=['GET'])
# def buscar_sala_por_numero(numero_sala):
#     sala = SalaController.buscar_por_numero(numero_sala)
#     if sala:
#         return jsonify({
#             'id_sala': sala.get_id_sala(),
#             'numero_sala': sala.numero_sala,
#             'local': sala.local,
#             'classificacao': sala.classificacao
#         }), 200
#     return jsonify({'message': 'Sala não encontrada'}), 404