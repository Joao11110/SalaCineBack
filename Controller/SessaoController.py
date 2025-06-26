from datetime import datetime
from Model.Sessao import Sessao
from Controller.FilmeController import FilmeController
from Controller.SalaController import SalaController

class SessaoController:
    @staticmethod
    def agendar(id_filme, id_sala, data_hora):
        filme = FilmeController.get_by_id(id_filme)
        sala = SalaController.get_by_id(id_sala)

        if not filme or not sala:
            return None

        if filme.classificacao > sala.classificacao:
            return None

        if Sessao.listar_por_sala_e_horario(sala, data_hora):
            return None

        return Sessao.cadastrar_filme(filme, sala, data_hora)

    @staticmethod
    def listar_por_data(data=None):
        return Sessao.listar_por_data(data)

    @staticmethod
    def get_by_id(id_sessao):
        return Sessao.get_or_none(Sessao.id_sessao == id_sessao)