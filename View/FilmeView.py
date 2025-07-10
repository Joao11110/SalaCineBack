from flask import Blueprint, request, jsonify
from Controller.FilmeController import FilmeController
from datetime import datetime

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/filmes', methods=['POST'])
def createFilme():
    data = request.get_json()

    required_fields = ['titulo', 'duracao', 'classificacao', 'diretor', 'genero']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400

    try:
        filme = FilmeController.cadastrar(
            titulo=data['titulo'],
            duracao=int(data['duracao']),
            classificacao=int(data['classificacao']),
            diretor=data['diretor'],
            genero=data['genero'],
        )
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos', 'details': str(e)}), 400

    return jsonify({
        'message': 'Filme cadastrado com sucesso.',
        'filme': {
            'id_filme': filme.id_filme,
            'titulo': filme.titulo,
            'duracao': filme.duracao,
            'classificacao': filme.classificacao,
            'genero': filme.genero,
            'diretor': filme.diretor,
            'data_cadastro': datetime.now().isoformat()
        }
    }), 201

@filme_bp.route('/filmes', methods=['GET'])
def readFilmes():
    try:
        filmes = FilmeController.read()

        if not filmes:
            return jsonify({'error': 'Não há filmes cadastrados.'}), 404

        return jsonify([{
            'id_filme': f.id_filme,
            'titulo': f.titulo,
            'duracao': f.duracao,
            'classificacao': f.classificacao,
            'diretor': f.diretor,
            'genero': f.genero
        } for f in filmes]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes/<int:id_filme>', methods=['GET'])
def readFilmesById(id_filme):
    try:
        filme = FilmeController.readById(id_filme)

        if not filme:
            return jsonify({'error': 'Filme não encontrado.'}), 404

        return jsonify({
            'id_filme': filme.id_filme,
            'titulo': filme.titulo,
            'duracao': filme.duracao,
            'classificacao': filme.classificacao,
            'diretor': filme.diretor,
            'genero': filme.genero,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @filme_bp.route('/filmes/<int:id_filme>', methods=['PUT'])
# def editar_filme(id_filme):
#     data = request.get_json()
#     updated = FilmeController.editar(id_filme, **data)
#     return jsonify({'updated': updated}), 200

# @filme_bp.route('/filmes/<int:id_filme>', methods=['DELETE'])
# def excluir_filme(id_filme):
#     deleted = FilmeController.excluir(id_filme)
#     return jsonify({'deleted': deleted}), 200