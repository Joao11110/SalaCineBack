from Model.Sala import Sala

class SalaController:
    @staticmethod
    def create(numero_sala=int, local=str):
        return Sala.create(numero_sala, local)

    @staticmethod
    def read():
        salas = Sala.select().order_by(Sala.id_sala)
        return [cls._formatSalaOutput(salas) for sala in salas]

    @staticmethod
    def readByNumero(numero_sala=int):
        sala =  Sala.readByNumero(numero_sala)
        return cls._formatSalaOutput(sala)

    @staticmethod
    def readById(id_sala=int):
        sala = Sala.get_or_none(Sala.id_sala == id_sala)
        return cls._formatSalaOutput(sala)

    @staticmethod
    def update(id_sala=int, **kwargs):
        return Sala.update(id_sala, **kwargs)

    @staticmethod
    def delete(id_sala=int):
        return Sala.delete(id_sala)

    @staticmethod
    def _formatSalaOutput(cls, sala) -> dict:
        return {
            'id_sala': sala.id_sala,
            'numero_sala': sala.numero_sala,
            'local': sala.local,
        }