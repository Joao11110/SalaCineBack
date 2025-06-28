from flask import Blueprint, request, jsonify
from Controller.FilmeController import FilmeController

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/filmes', methods=['POST'])
def cadastrar_filme():
    data = request.get_json()

    required_fields = ['titulo', 'duracao', 'classificacao', 'genero', 'diretor']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400
    
    try:
        filme = FilmeController.cadastrar(
            titulo=data['titulo'],
            duracao=int(data['duracao']),
            classificacao=int(data['classificacao']),
            genero=data['genero'],
            diretor=data['diretor']
        )
    except ValueError as e:
        return jsonify({'error': 'Dados inválidos', 'details': str(e)}), 400

    return jsonify({
        'message': 'Filme cadastrado com sucesso',
        'filme': {
            'id_filme': filme.get_id_filme(),
            'titulo': filme.titulo,
            'duracao': filme.duracao,
            'classificacao': filme.classificacao,
            'genero': filme.genero,
            'diretor': filme.diretor,
            'data_cadastro': datetime.now().isoformat()
        }
    }), 201

# @filme_bp.route('/filmes/<int:id_filme>', methods=['PUT'])
# def editar_filme(id_filme):
#     data = request.get_json()
#     updated = FilmeController.editar(id_filme, **data)
#     return jsonify({'updated': updated}), 200

# @filme_bp.route('/filmes/<int:id_filme>', methods=['DELETE'])
# def excluir_filme(id_filme):
#     deleted = FilmeController.excluir(id_filme)
#     return jsonify({'deleted': deleted}), 200

# @filme_bp.route('/filmes', methods=['GET'])
# def buscar_filmes():
#     titulo = request.args.get('titulo', '')
#     filmes = FilmeController.buscar_por_titulo(titulo)
#     return jsonify([{
#         'id_filme': f.get_id_filme(),
#         'titulo': f.titulo,
#         'duracao': f.duracao,
#         'classificacao': f.classificacao,
#         'genero': f.genero,
#         'diretor': f.diretor
#     } for f in filmes]), 200