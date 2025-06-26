from flask import Blueprint, request, jsonify
from Controller.FilmeController import FilmeController

filme_bp = Blueprint('filme', __name__)

@filme_bp.route('/filmes', methods=['POST'])
def cadastrar_filme():
    data = request.get_json()
    filme = FilmeController.cadastrar(
        titulo=data['titulo'],
        duracao=data['duracao'],
        classificacao=data['classificacao'],
        genero=data['genero'],
        diretor=data['diretor']
    )
    return jsonify({'id_filme': filme.get_id_filme()}), 201

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