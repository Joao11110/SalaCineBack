from flask import Blueprint, request, jsonify
from datetime import datetime
from Controller.SessaoController import SessaoController

sessao_bp = Blueprint('sessao', __name__)
@sessao_bp.route('/sessoes', methods=['POST'])
def createSessao():
    data = request.get_json()

    required_fields = ['data_hora', 'filme_id', 'sala_id']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Missing required fields',
            'required': required_fields
        }), 400

    try:
        data_hora = datetime.fromisoformat(data['data_hora'])
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    try:
        sessao = SessaoController.create(
            data_hora=data_hora,
            filme_id=data['filme_id'],
            sala_id=data['sala_id']
        )
        return jsonify({
            'message': 'Session created successfully',
            'session': {
                'id': sessao.id_sessao,
                'datetime': sessao.data_hora.isoformat(),
                'filme_id': sessao.filme.id_filme,
                'sala_id': sessao.sala.id_sala
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@sessao_bp.route('/sessoes', methods=['GET'])
def readSessoes():
    try:
        sessoes = list(SessaoController.read())

        if not sessoes:
            return jsonify({
                'message': 'Nenhuma sessão encontrada',
                'data': [],
                'count': 0
            }), 200

        formatted_sessoes = [SessaoController._formatSessaoOutput(s) for s in sessoes]
        
        return jsonify({
            'message': 'Sessões recuperadas com sucesso',
            'data': formatted_sessoes,
            'count': len(formatted_sessoes)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e),
            'data': None
        }), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': 'Erro interno ao buscar sessões',
            'data': None
        }), 500

@sessao_bp.route('/sessoes/<int:id_sessao>', methods=['GET'])
def readSessaoById(id_sessao):
    try:
        sessao = SessaoController.readById(id_sessao)
        if not sessao:
            return jsonify({
                'error': 'Sessão não encontrada',
                'data': None
            }), 404
            
        return jsonify({
            'message': 'Sessão recuperada com sucesso',
            'data': SessaoController._formatSessaoOutput(sessao)
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e),
            'data': None
        }), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': 'Erro interno ao buscar sessão',
            'data': None
        }), 500

@sessao_bp.route('/sessoes/<int:id_sessoes>', methods=['PUT'])
def updateSessao(id_sessao):
    try:
        data = request.get_json()
        sessao = SessaoController.update(id_sala, **data)
        return jsonify({'updated': updated}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 200

@sessao_bp.route('/sessoes/<int:id_sessao>', methods=['DELETE'])
def deleteSessao(id_sessao):
    try:
        sessao = SessaoController.readById(id_sessao)
        if not sessao:
            return jsonify({"error": "Sessão não foi encontrada, portanto não foi deletada"}), 404
        SalaController.delete(id_sessao)
        return jsonify({"deleted": "Sessão foi deletada com sucesso"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500