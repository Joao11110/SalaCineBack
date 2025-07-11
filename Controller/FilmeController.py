from peewee import DoesNotExist, JOIN
from Model.Filme import Filme, Genero, FilmeGenero
from Model.BaseModel import db

class FilmeController:
    @classmethod
    def cadastrar(cls, titulo: str, duracao: int, classificacao: int, diretor: str, 
                 generos_nomes: list, poster_file=None) -> Filme:
        try:
            with db.atomic():
                filme = Filme.create(
                    titulo=titulo,
                    duracao=duracao,
                    classificacao=classificacao,
                    diretor=diretor,
                    poster_blob=poster_file.read() if poster_file else None,
                    poster_mime_type=getattr(poster_file, 'content_type', None) if poster_file else None
                )

                if generos_nomes:
                    for genero_nome in generos_nomes:
                        genero, _ = Genero.get_or_create(nome=genero_nome.strip())
                        FilmeGenero.create(filme=filme, genero=genero)

                return filme
        except Exception as e:
            db.rollback()
            raise ValueError(f"Erro ao cadastrar filme: {str(e)}")

    @classmethod
    def read(cls) -> list[Filme]:
        """Get all movies with their genres"""
        query = (Filme
                .select(Filme, Genero)
                .join(FilmeGenero, JOIN.LEFT_OUTER)
                .join(Genero, JOIN.LEFT_OUTER)
                .order_by(Filme.titulo))

        result = []
        for filme in query:
            filme_data = {
                'id_filme': filme.id_filme,
                'titulo': filme.titulo,
                'duracao': filme.duracao,
                'classificacao': filme.classificacao,
                'diretor': filme.diretor,
                'generos': [g.nome for g in filme.generos()],
                'poster': filme.poster_blob is not None
            }
            result.append(filme_data)
        
        return result

    @classmethod
    def readById(cls, id_filme: int) -> dict:
        """Get movie by ID with genres"""
        try:
            filme = Filme.get(Filme.id_filme == id_filme)
            return {
                'id_filme': filme.id_filme,
                'titulo': filme.titulo,
                'duracao': filme.duracao,
                'classificacao': filme.classificacao,
                'diretor': filme.diretor,
                'generos': [g.nome for g in filme.generos()],
                'poster': filme.poster_blob is not None
            }
        except DoesNotExist:
            return None