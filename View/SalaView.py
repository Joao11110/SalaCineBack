from flask import Blueprint, request, jsonify
from Controller.SalaController import SalaController
from datetime import datetime

sala_bp = Blueprint('sala', __name__)

@sala_bp.route('/salas', methods=['POST'])
def createSala():
    data = request.get_json()

    required_fields = ['numero_sala', 'local']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Campos obrigatórios faltando',
            'required_fields': required_fields
        }), 400

    try:
        if SalaController.readByNumero(data['numero_sala']):
            return jsonify({
                'error': 'Número de sala já existe',
                'numero_sala': data['numero_sala']
            }), 409

        sala = SalaController.create(
            numero_sala=data['numero_sala'],
            local=data['local'],
        )

    except ValueError as e:
        return jsonify({
            'error': 'Dados inválidos',
            'details': str(e)
        }), 400

    return jsonify({
        'message': 'Sala cadastrada com sucesso.',
        'sala': {
            'id_sala': sala.id_sala,
            'numero_sala': sala.numero_sala,
            'local': sala.local,
        }
    }), 201

@sala_bp.route('/salas', methods=['GET'])
def readSalas():
    try:

        sala = list(SalaController.read())

        if not sala:
            return jsonify({'message': 'Não há salas cadastradas.'}), 404

        return jsonify([{
            'id_sala': sala.id_sala,
            'numero_sala': sala.numero_sala,
            'local': sala.local
        } for sala in sala]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['GET'])
def readSalaById(id_sala):
    try:

        sala = SalaController.readById(id_sala)

        if not sala:
            return jsonify({'error': 'Sala não encontrada'}), 404

        return jsonify({
            'id_sala': sala.id_sala,
            'numero_sala': sala.numero_sala,
            'local': sala.local,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:numero_sala>', methods=['GET'])
def readSalaByNumber(numero_sala):
    try:

        sala = SalaController.readByNumero(numero_sala)

        if not sala:
            return jsonify({'message': 'Sala não foi encontrada.'}), 404

        return jsonify({
            'id_sala': sala.get_id_sala(),
            'numero_sala': sala.numero_sala,
            'local': sala.local
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @sala_bp.route('/salas/<int:id_sala>', methods=['PUT'])
# def editar_sala(id_sala):
#     data = request.get_json()
#     updated = SalaController.editar(id_sala, **data)
#     return jsonify({'updated': updated}), 200

# @sala_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
# def excluir_sala(id_sala):
#     deleted = SalaController.excluir(id_sala)
#     return jsonify({'deleted': deleted}), 200