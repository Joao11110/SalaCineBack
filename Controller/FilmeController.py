from Model.Filme import Filme

class FilmeController:
    @staticmethod
    def create(titulo=str, duracao=int, classificacao=int, diretor=str, genero=str):
        return Filme.create(titulo, duracao, classificacao, diretor, genero)

    @staticmethod
    def read():
        return Filme.select()

    @staticmethod
    def readByTitulo(titulo=str):
        return Filme.readByTitulo(titulo)

    @staticmethod
    def readById(id_filme=int):
        return Filme.get_or_none(Filme.id_filme == id_filme)

    @staticmethod
    def update(id_filme=int, **kwargs):
        return Filme.update(id_filme, **kwargs)

    @staticmethod
    def delete(id_filme=int):
        return Filme.delete(id_filme)


