from Model.Sala import Sala

class SalaController:
    @staticmethod
    def cadastrar(numero_sala=int, local=str, classificacao=int):
        return Sala.cadastrar_sala(numero_sala, local, classificacao)

    @staticmethod
    def editar(id_sala=int, **kwargs):
        return Sala.editar_sala(id_sala, **kwargs)

    @staticmethod
    def excluir(id_sala=int):
        return Sala.excluir_sala(id_sala)

    @staticmethod
    def buscar_por_numero(numero_sala=int):
        return Sala.buscar_por_numero(numero_sala)

    @staticmethod
    def get_by_id(id_sala=int):
        return Sala.get_or_none(Sala.id_sala == id_sala)