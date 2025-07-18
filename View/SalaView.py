from Controller.SalaController import SalaController
from flask import Blueprint, request, jsonify
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
        'message': 'Sala foi cadastrada com sucesso.',
        'sala': SalaController._formatSalaOutput(sala)
    }), 200

@sala_bp.route('/salas', methods=['GET'])
def readSalas():
    try:
        salas = SalaController.read()
        if not salas:
            return jsonify({"error": "Não há salas cadastradas"}), 404
        return jsonify({
            'message': 'Salas recuperadas com sucesso',
            'salas': salas,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['GET'])
def readSalaById(id_sala=int):
    try:
        sala = SalaController.readById(id_sala)
        if not sala:
            return jsonify({"error": "Sala não foi encontrada"}), 404
        return jsonify({
            'message': 'Sala recuperada com sucesso',
            'salas': sala,
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:numero_sala>', methods=['GET'])
def readSalaByNumber(numero_sala=int):
    try:
        sala = SalaController.readByNumero(numero_sala)
        if not sala:
            return jsonify({"error": "Sala não foi encontrada"}), 404
        return jsonify({
            'message': 'Sala recuperada com sucesso',
            'sala': sala
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['PUT'])
def updateSala(id_sala=int):
    data = request.get_json()

    try:
        if 'numero_sala' in data:
            try:
                data['numero_sala'] = int(data['numero_sala'])
            except (ValueError, TypeError):
                return jsonify({
                    'error': 'numero_sala deve ser um número inteiro'
                }), 400

        sala = SalaController.update(id_sala, **data)
        return jsonify({
            'message': 'Sala foi atualizada com sucesso',
            'sala': sala
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sala_bp.route('/salas/<int:id_sala>', methods=['DELETE'])
def deleteSala(id_sala=int):
    try:
        deleted = SalaController.delete(id_sala)
        if not deleted:
            return jsonify({"error": "Sala não encontrada, portanto não foi deletada"}), 404
        return jsonify({"message": "Sala deletada com sucesso"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({
            "error": "Erro ao deletar sala",
            "details": str(e)
        }), 500