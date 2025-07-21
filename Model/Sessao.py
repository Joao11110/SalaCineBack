from peewee import AutoField, DateTimeField, ForeignKeyField, DoesNotExist
from Model.BaseModel import BaseModel
from datetime import datetime
from Model.Filme import Filme
from Model.Sala import Sala

class Sessao(BaseModel):
    id_sessao = AutoField(primary_key=True)
    data_hora = DateTimeField()
    filme = ForeignKeyField(Filme, backref='sessoes')
    sala = ForeignKeyField(Sala, backref='sessoes')

    @classmethod
    def create(cls, data_hora=str, filme=int, sala=int):
        return super().create(
            data_hora=data_hora,
            filme=filme,
            sala=sala
        )

    @classmethod
    def readByDate(cls, data=None):
        query = cls.select()
        if data:
            query = query.where(cls.data_hora.date() == data.date())
        return query.order_by(cls.data_hora)

    @classmethod
    def readBySalaAndDate(cls, sala, data_hora=str):
        return cls.select().where(
            (cls.sala == sala) &
            (cls.data_hora == data_hora)
        ).exists()

    @classmethod
    def update(cls, id_sessao=int, **kwargs):
        with super()._meta.database.atomic():
            sessao = cls.get_or_none(cls.id_sessao == id_sessao)
            if not sessao:
                raise DoesNotExist("Sessão não foi encontrada")

            query = super().update(**kwargs).where(cls.id_sessao == id_sessao)
            updated = query.execute()

            return cls.get(cls.id_sessao == id_sessao)

    @classmethod
    def delete(cls, id_sessao):
        with super()._meta.database.atomic():
            sessao = cls.get_or_none(cls.id_sessao == id_sessao)
            if not sessao:
                raise DoesNotExist("Sessão não foi encontrada")

            query = super().delete().where(cls.id_sessao == id_sessao)
            return query.execute()

    @classmethod
    def getIdSessao(self):
        return self.id_sessao