from flask import Blueprint, request, jsonify
from Controller.FilmeController import FilmeController, Genero
from peewee import DoesNotExist
from io import BytesIO
from flask import send_file

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/filmes', methods=['POST'])
def createFilme():
    if request.is_json:
        data = request.get_json()
        poster_file = None
    else:
        data = request.form
        poster_file = request.files.get('poster')

    required_fields = ['titulo', 'duracao', 'classificacao', 'diretor', 'generos']
    if not all(field in data for field in required_fields):
        return jsonify({
            'error': 'Campos obrigatórios faltando',
            'required_fields': required_fields
        }), 400

    try:
        generos = data['generos']
        if isinstance(generos, str):
            generos = [g.strip() for g in generos.split(',') if g.strip()]
        elif not isinstance(generos, list):
            generos = []

        filme = FilmeController.cadastrar(
            titulo=data['titulo'],
            duracao=int(data['duracao']),
            classificacao=int(data['classificacao']),
            diretor=data['diretor'],
            generos_nomes=generos,
            poster_file=poster_file
        )

        return jsonify({
            'message': 'Filme cadastrado com sucesso',
            'filme': FilmeController._formatFilmeOutput(filme)
            }), 201

    except ValueError as e:
        return jsonify({'error': 'Dados inválidos', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes', methods=['GET'])
def readFilmes():
    try:
        filmes = FilmeController.read()
        if not filmes:
            return jsonify({"error": "Não há filmes cadastrados"}), 404
        return jsonify(filmes), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes/<int:id_filme>', methods=['GET'])
def readFilmeById(id_filme):
    try:
        filme = FilmeController.readById(id_filme)
        if not filme:
            return jsonify({"error": "Filme não foi encontrado"}), 404
        return jsonify(filme), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes/<int:id_filme>/poster', methods=['GET'])
def readPoster(id_filme):
    try:
        filme = FilmeController.readById(id_filme)

        if not filme or not filme.get('poster'):
            return jsonify({'error': 'Pôster não foi encontrado'}), 404

        filmeInstance = Filme.get(Filme.id_filme == id_filme)
        return send_file(
            BytesIO(filmeInstance.poster_blob),
            mimetype=filmeInstance.poster_mime_type
        )

    except DoesNotExist:
        return jsonify({'error': 'Poster do filme não foi encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/generos', methods=['GET'])
def readGeneros():
    try:
        generos = Genero.select()

        if not generos:
            return jsonify({'error': 'Nenhum gênero foi encontrado'}), 404

        return jsonify([g.nome for g in generos]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes/<int:id_filme>', methods=['PUT'])
def updateFilme(id_filme):
    data = request.get_json()

    try:
        if 'generos' in data and isinstance(data['generos'], str):
            data['generos'] = [g.strip() for g in data['generos'].split(',')]
        
        filme = FilmeController.update(
            id_filme=id_filme,
            **data
        )

        return jsonify({
            'message': 'Filme atualizado com sucesso',
            'filme': FilmeController._formatFilmeOutput(filme)
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@filme_bp.route('/filmes/<int:id_filme>', methods=['DELETE'])
def excluirFilme(id_filme):
    try:
        filme = FilmeController.readById(id_filme)
        if not filme:
            return jsonify({"error": "Filme não foi encontrado, portando não foi deletado"}), 404
        FilmeController.delete(id_filme)
        return jsonify({"deleted": "Filme foi deletado com sucesso"}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500