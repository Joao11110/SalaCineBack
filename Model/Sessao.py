from peewee import Model, AutoField, DateTimeField, ForeignKeyField
from datetime import datetime
from Model.BD import db
from Model.Filme import Filme
from Model.Sala import Sala

class BaseModel(Model):
    class Meta:
        database = db

class Sessao(BaseModel):
    id_sessao = AutoField(primary_key=True)
    data_hora = DateTimeField()
    filme = ForeignKeyField(Filme, backref='sessoes')
    sala = ForeignKeyField(Sala, backref='sessoes')

    @classmethod
    def cadastrar_filme(cls, filme, sala, data_hora):
        return cls.create(
            filme=filme,
            sala=sala,
            data_hora=data_hora
        )

    @classmethod
    def listar_por_data(cls, data=None):
        query = cls.select()
        if data:
            query = query.where(cls.data_hora.date() == data.date())
        return query.order_by(cls.data_hora)

    def get_id_sessao(self):
        return self.id_sessao

    @classmethod
    def listar_por_sala_e_horario(cls, sala, data_hora):
        return cls.select().where(
            (cls.sala == sala) &
            (cls.data_hora == data_hora)
        ).exists()

    @classmethod
    def editar_filme(cls, id_filme=int, **kwargs):
        query = cls.update(**kwargs).where(cls.id_filme == id_filme)
        return query.execute()

    @classmethod
    def excluir_filme(cls, id_filme=int):
        return cls.delete().where(cls.id_filme == id_filme).execute()