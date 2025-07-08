from Model.Sala import Sala

class SalaController:
    @staticmethod
    def create(numero_sala=int, local=str):
        return Sala.create(numero_sala, local)

    @staticmethod
    def read():
        return Sala.select()

    @staticmethod
    def readByNumero(numero_sala=int):
        return Sala.readByNumero(numero_sala)

    @staticmethod
    def readById(id_sala=int):
        return Sala.get_or_none(Sala.id_sala == id_sala)

    @staticmethod
    def update(id_sala=int, **kwargs):
        return Sala.update(id_sala, **kwargs)

    @staticmethod
    def delete(id_sala=int):
        return Sala.delete(id_sala)