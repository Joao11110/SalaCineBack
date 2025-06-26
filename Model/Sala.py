from peewee import Model, AutoField, IntegerField, CharField
from Model.BD import db

class BaseModel(Model):
    class Meta:
        database = db

class Sala(BaseModel):
    id_sala = AutoField(primary_key=True)
    numero_sala = IntegerField(unique=True)
    local = CharField(max_length=100)
    classificacao = IntegerField()

    @classmethod
    def cadastrar_sala(cls, numero_sala=int, local=str, classificacao=int):
        return cls.create(
            numero_sala=numero_sala,
            local=local,
            classificacao=classificacao
        )

    @classmethod
    def buscar_por_numero(cls, numero_sala=int):
        return cls.get_or_none(cls.numero_sala == numero_sala)

    def get_id_sala(self):
        return self.id_sala

    @classmethod
    def editar_sala(cls, id_sala=int, **kwargs):
        query = cls.update(**kwargs).where(cls.id_sala == id_sala)
        return query.execute()

    @classmethod
    def excluir_sala(cls, id_sala=int):
        return cls.delete().where(cls.id_sala == id_sala).execute()
