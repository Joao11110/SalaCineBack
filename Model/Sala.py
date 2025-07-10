from peewee import Model, AutoField, IntegerField, CharField
from Model.BaseModel import BaseModel

class Sala(BaseModel):
    id_sala = AutoField(primary_key=True)
    numero_sala = IntegerField(unique=True)
    local = CharField(max_length=100)

    @classmethod
    def create(cls, numero_sala=int, local=str):
        return cls.create(
            numero_sala=numero_sala,
            local=local,
        )

    @classmethod
    def readByNumero(cls, numero_sala=int):
        return cls.get_or_none(cls.numero_sala == numero_sala)

    @classmethod
    def readIdSala(self):
        return self.id_sala

    @classmethod
    def update(cls, id_sala=int, **kwargs):
        query = cls.update(**kwargs).where(cls.id_sala == id_sala)
        return query.execute()

    @classmethod
    def delete(cls, id_sala=int):
        return cls.delete().where(cls.id_sala == id_sala).execute()
