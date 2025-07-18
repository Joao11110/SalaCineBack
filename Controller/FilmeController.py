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
    def read(cls) -> list[dict]:
        """Get all movies with their genres (without duplicates)"""
        filmes = Filme.select().order_by(Filme.titulo)
        return [cls._formatFilmeOutput(filme) for filme in filmes]

    @classmethod
    def readById(cls, id_filme: int) -> dict:
        """Get movie by ID with genres"""
        try:
            filme = Filme.get(Filme.id_filme == id_filme)
            return cls._formatFilmeOutput(filme)
        except DoesNotExist:
            return None

    @staticmethod
    def update(id_filme, **kwargs):
        try:
            return Filme.update(id_filme, **kwargs)

        except DoesNotExist as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error updating movie: {str(e)}")
        except DoesNotExist:
            db.rollback()
            raise ValueError("Filme não encontrado")
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error updating movie: {str(e)}")

    @staticmethod
    def delete(id_filme=int):
        return Filme.delete(id_filme)

    @classmethod
    def _formatFilmeOutput(cls, filme) -> dict:
        return {
            'id_filme': filme.id_filme,
            'titulo': filme.titulo,
            'duracao': filme.duracao,
            'classificacao': filme.classificacao,
            'diretor': filme.diretor,
            'generos': [g.nome for g in filme.generos()],
            'poster': filme.poster_blob is not None,
            'poster_url': f"/api/filmes/{filme.id_filme}/poster" if filme.poster_blob else None
        }