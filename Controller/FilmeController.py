from Model.Filme import Filme

class FilmeController:
    @staticmethod
    def cadastrar(titulo=str, duracao=int, classificacao=int, genero=str, diretor=str):
        return Filme.cadastrar_filme(titulo, duracao, classificacao, genero, diretor)

    @staticmethod
    def editar(id_filme=int, **kwargs):
        return Filme.editar_filme(id_filme, **kwargs)

    @staticmethod
    def excluir(id_filme=int):
        return Filme.excluir_filme(id_filme)

    @staticmethod
    def buscar_por_titulo(titulo=str):
        return Filme.buscar_por_titulo(titulo)

    @staticmethod
    def get_by_id(id_filme=int):
        return Filme.get_or_none(Filme.id_filme == id_filme)