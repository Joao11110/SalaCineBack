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
        'sala': SalaController._formatSalaOutput(sala)
    }), 201

@sala_bp.route('/salas', methods=['GET'])
def readSalas():
    try:
        salas = SalaController.read()
        if not salas:
            return jsonify({"error": "Não há salas cadastradas"}), 404
        return jsonify(salas), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['GET'])
def readSalaById(id_sala):
    try:
        sala = SalaController.readById(id_sala)
        if not sala:
            return jsonify({"error": "Sala não foi encontrada"}), 404
        return jsonify(sala), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:numero_sala>', methods=['GET'])
def readSalaByNumber(numero_sala):
    try:
        sala = SalaController.readByNumero(numero_sala)
        if not sala:
            return jsonify({"error": "Sala não foi encontrada"}), 404
        return jsonify(sala), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['PUT'])
def updateSala(id_sala):
    try:
        data = request.get_json()
        updated = SalaController.update(id_sala, **data)
        return jsonify({'updated': updated}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
def deleteSala(id_sala):
    try:
        sala = SalaController.readById(id_sala)
        if not sala:
            return jsonify({"error": "Sala não foi encontrada, portanto não foi deletada"}), 404
        SalaController.delete(id_sala)
        return jsonify({"deleted": "Sala foi deletada com sucesso"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500