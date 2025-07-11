from flask import Blueprint, request, jsonify
from datetime import datetime
from Controller.SessaoController import SessaoController

sessao_bp = Blueprint('sessao', __name__)

@sessao_bp.route('/sessoes', methods=['POST'])
def createSessao():
    data = request.get_json()

    try:
        data_hora = datetime.fromisoformat(data['data_hora'])
    except (ValueError, KeyError):
        return jsonify({'error': 'Formato de data/hora inválido.'}), 400

    required_fields = ['data_hora', 'filme_id', 'sala_id']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Campos obrigatórios faltando',
            'required_fields': required_fields,
            'received_data': data
        }), 400

    try:
        sessao = SessaoController.create(
            data_hora=data_hora,
            id_filme=data['filme_id'],
            id_sala=data['sala_id']
        )

        if not sessao:
            return jsonify({'error': 'Não foi possível agendar a sessão.'}), 400

        return jsonify({
            'message': 'Sessão cadastrada com sucesso.',
            'sessao': {
                'id_sessao': sessao.id_sessao,
                'data_hora': sessao.data_hora.isoformat(),
                'filme_id': sessao.filme.id_filme,
                'sala_id': sessao.sala.id_sala
            }
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@sessao_bp.route('/sessoes', methods=['GET'])
def readSessoes():
    try:
        data_str = request.args.get('data')
        data = datetime.fromisoformat(data_str) if data_str else None
        sessoes = SessaoController.readByData(data)

        if not sessoes:
            return jsonify({'message': 'Não há sessões cadastradas.'}), 404

        return jsonify([{
            'id_sessao': s.get_id_sessao(),
            'data_hora': s.data_hora.isoformat(),
            'filme': {
                'id_filme': s.filme.get_id_filme(),
                'titulo': s.filme.titulo
            },
            'sala': {
                'id_sala': s.sala.get_id_sala(),
                'numero_sala': s.sala.numero_sala
            }
        } for s in sessoes]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessao_bp.route('/sessoes/<int:id_sessao>', methods=['GET'])
def readSessaoById(id_sessao):
    try:

        sessao = SessaoController.readById(id_sessao)

        if not sessao:
            return jsonify({'error': 'Sessão não encontrada'}), 404

        return jsonify({
            'id_sessao': sessao.id_sessao,
            'data_hora': sessao.data_hora.isoformat(),
            'filme': {
                'id_filme': sessao.filme.id_filme,
                'titulo': sessao.filme.titulo
            },
            'sala': {
                'id_sala': sessao.sala.id_sala,
                'numero_sala': sessao.sala.numero_sala
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500