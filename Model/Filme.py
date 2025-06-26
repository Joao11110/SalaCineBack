from peewee import Model, AutoField, CharField, IntegerField, CharField
from Model.BD import db

class BaseModel(Model):
    class Meta:
        database = db

class Filme(BaseModel):
    id_filme = AutoField(primary_key=True)
    titulo = CharField(max_length=100)
    duracao = IntegerField()
    classificacao = IntegerField()
    genero = CharField(max_length=50)
    diretor = CharField(max_length=100)

    @classmethod
    def cadastrar_filme(cls, titulo=str, duracao=int, classificacao=int, genero=str, diretor=str):
        return cls.create(
            titulo=titulo,
            duracao=duracao,
            classificacao=classificacao,
            genero=genero,
            diretor=diretor
        )

    @classmethod
    def buscar_por_titulo(cls, titulo=str):
        return cls.select().where(cls.titulo.contains(titulo))

    def get_id_filme(self):
        return self.id_filme

    @classmethod
    def editar_filme(cls, id_filme=int, **kwargs):
        query = cls.update(**kwargs).where(cls.id_filme == id_filme)
        return query.execute()

    @classmethod
    def excluir_filme(cls, id_filme=int):
        return cls.delete().where(cls.id_filme == id_filme).execute()
