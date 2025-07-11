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
            'filme': {
                'id_filme': filme.id_filme,
                'titulo': filme.titulo,
                'duracao': filme.duracao,
                'classificacao': filme.classificacao,
                'diretor': filme.diretor,
                'generos': [g.nome for g in filme.generos()],
                'poster_url': f'/api/filmes/{filme.id_filme}/poster' if filme.poster_blob else None,
                'data_cadastro': filme.data_cadastro.isoformat() if hasattr(filme, 'data_cadastro') else None
            }
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
            return jsonify({'error': 'Não há filmes cadastrados'}), 404

        return jsonify(filmes), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes/<int:id_filme>', methods=['GET'])
def readFilmesById(id_filme):
    try:
        filme = FilmeController.readById(id_filme)

        if not filme:
            return jsonify({'error': 'Filme não encontrado'}), 404

        return jsonify(filme), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@filme_bp.route('/filmes/<int:id_filme>/poster', methods=['GET'])
def readPoster(id_filme):
    try:
        filme = FilmeController.readById(id_filme)

        if not filme or not filme.get('poster'):
            return jsonify({'error': 'Pôster não foi encontrado'}), 404

        # Get the actual model instance for the poster data
        filme_instance = Filme.get(Filme.id_filme == id_filme)
        return send_file(
            BytesIO(filme_instance.poster_blob),
            mimetype=filme_instance.poster_mime_type
        )

    except DoesNotExist:
        return jsonify({'error': 'Filme não encontrado'}), 404
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

# @filme_bp.route('/filmes/<int:id_filme>', methods=['PUT'])
# def editar_filme(id_filme):
#     data = request.get_json()
#     updated = FilmeController.editar(id_filme, **data)
#     return jsonify({'updated': updated}), 200

# @filme_bp.route('/filmes/<int:id_filme>', methods=['DELETE'])
# def excluir_filme(id_filme):
#     deleted = FilmeController.excluir(id_filme)
#     return jsonify({'deleted': deleted}), 200