from Controller.SessaoController import SessaoController
from flask import Blueprint, request, jsonify
from datetime import datetime

sessao_bp = Blueprint('sessao', __name__)
@sessao_bp.route('/sessoes', methods=['POST'])
def createSessao():
    data = request.get_json()

    required_fields = ['data_hora', 'filme_id', 'sala_id']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Parâmetros insuficientes',
            'required': required_fields
        }), 400

    try:
        data_hora = datetime.fromisoformat(data['data_hora'])
    except ValueError:
        return jsonify({'error': 'Formato de data e hora incorretos'}), 400

    try:
        sessao = SessaoController.create(
            data_hora=data_hora,
            filme_id=data['filme_id'],
            sala_id=data['sala_id']
        )
        return jsonify({
            'message': 'Sessão foi criada com sucesso',
            'sessão': SessaoController._formatSessaoOutput(sessao)
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessao_bp.route('/sessoes', methods=['GET'])
def readSessoes():
    try:
        sessoes = list(SessaoController.read())

        if not sessoes:
            return jsonify({'message': 'Não há sessoes cadastradas'}), 200

        sessoes = [SessaoController._formatSessaoOutput(s) for s in sessoes]

        return jsonify({
            'message': 'Sessões recuperadas com sucesso',
            'data': sessoes,
        }), 200

    except ValueError as e:
        return jsonify({
            'error': str(e),
            'data': None
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Erro interno ao buscar sessões',
            'details': str(e)
        }), 500

@sessao_bp.route('/sessoes/<int:id_sessao>', methods=['GET'])
def readSessaoById(id_sessao):
    try:
        sessao = SessaoController.readById(id_sessao)

        return jsonify({
            'sessão': SessaoController._formatSessaoOutput(sessao),
            'message': 'Sessão recuperada com sucesso'
        }), 200

    except ValueError as e:
        return jsonify({
            'data': None,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'sessao': None,
            'error': 'Erro interno no servidor'
        }), 500

@sessao_bp.route('/sessoes/<int:id_sessao>', methods=['PUT'])
def updateSessao(id_sessao):
    try:
        data = request.get_json()

        for field in ['data_hora', 'filme_id', 'sala_id']:
            if field in data and data[field] == "":
                data[field] = None

        sessao = SessaoController.update(id_sessao, **data)

        return jsonify({
            'message': 'Sessão foi atualizada com sucesso',
            'sessao': SessaoController._formatSessaoOutput(sessao)
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({
            'error': 'Erro interno ao atualizar sessão',
            'details': str(e)
        }), 500

@sessao_bp.route('/sessoes/<int:id_sessao>', methods=['DELETE'])
def deleteSessao(id_sessao=int):
    try:
        sessao = SessaoController.delete(id_sessao)
        if not sessao:
            return jsonify({"error": "Sessão não encontrada, portanto não foi deletada"}), 404
        return jsonify({
            "message": "Sessão deletada com sucesso",
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({
            "error": "Erro ao deletar sessão",
            "details": str(e)
        }), 500