from datetime import datetime
from Model.Sessao import Sessao
from Controller.FilmeController import FilmeController
from Controller.SalaController import SalaController

class SessaoController:
    @staticmethod
    def create(id_filme=int, id_sala=int, data_hora=str):
        return Sessao.create(filme, sala, data_hora)

    @staticmethod
    def read(data=None):
        return Sessao.select()

    @staticmethod
    def readByData(data=None):
        return Sessao.readByDate(data)

    @staticmethod
    def readById(id_sessao):
        return Sessao.get_or_none(Sessao.id_sessao == id_sessao)

    @staticmethod
    def update(id_sala=int, **kwargs):
        return Sessao.update(id_sessao, **kwargs)

    @staticmethod
    def delete(id_sala=int):
        return Sessao.delete(id_sessao)