from peewee import Model, AutoField, CharField, IntegerField, CharField
from Model.BaseModel import BaseModel

class Filme(BaseModel):
    id_filme = AutoField(primary_key=True)
    titulo = CharField(max_length=150)
    duracao = IntegerField()
    classificacao = IntegerField()
    diretor = CharField(max_length=150)
    genero = CharField(max_length=50)

    @classmethod
    def create(cls, titulo=str, duracao=int, classificacao=int, diretor=str, genero=str):
        return cls.create(
            titulo=titulo,
            duracao=duracao,
            classificacao=classificacao,
            diretor=diretor,
            genero=genero
        )

    @classmethod
    def readByTitulo(cls, titulo=str):
        return cls.select().where(cls.titulo.contains(titulo))

    @classmethod
    def update(cls, id_filme=int, **kwargs):
        query = cls.update(**kwargs).where(cls.id_filme == id_filme)
        return query.execute()

    @classmethod
    def delete(cls, id_filme=int):
        return cls.delete().where(cls.id_filme == id_filme).execute()

    @classmethod
    def getIdFilme(self):
        return self.id_filme