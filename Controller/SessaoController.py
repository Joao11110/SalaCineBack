from datetime import datetime
from Model.Sessao import Sessao
from Controller.FilmeController import FilmeController
from Controller.SalaController import SalaController
from Model.Filme import Filme
from Model.Sala import Sala
from peewee import DoesNotExist

class SessaoController:
    @staticmethod
    def create(data_hora, filme_id, sala_id):
        try:
            with Sessao._meta.database.atomic():
                filme = Filme.get(Filme.id_filme == filme_id)
                sala = Sala.get(Sala.id_sala == sala_id)

                sessao = Sessao.create(
                    data_hora=data_hora,
                    filme=filme,
                    sala=sala
                )
                return sessao

        except DoesNotExist:
            raise ValueError("Filme ou Sala não encontrado")
        except Exception as e:
            raise ValueError(f"Error creating session: {str(e)}")

    @staticmethod
    def read():
        try:
            return (Sessao
                    .select(Sessao, Filme, Sala)
                    .join(Filme, on=(Sessao.filme == Filme.id_filme))
                    .join(Sala, on=(Sessao.sala == Sala.id_sala))
                    .order_by(Sessao.data_hora)
                    .objects())
        except Exception as e:
            print(f"Error in read: {str(e)}")
            raise ValueError(f"Error reading sessions: {str(e)}")

    @staticmethod
    def readById(id_sessao):
        try:
            return (Sessao
                    .select(Sessao, Filme, Sala)
                    .join(Filme, on=(Sessao.filme == Filme.id_filme))
                    .join(Sala, on=(Sessao.sala == Sala.id_sala))
                    .where(Sessao.id_sessao == id_sessao)
                    .objects()
                    .get())
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error in readById: {str(e)}")
            raise ValueError(f"Error reading session: {str(e)}")

    @staticmethod
    def readByData(data=None):
        return Sessao.readByDate(data)

    @staticmethod
    def update(id_sala=int, **kwargs):
        return Sessao.update(id_sessao, **kwargs)

    @staticmethod
    def delete(id_sala=int):
        return Sessao.delete(id_sessao)

    @staticmethod
    def _formatSessaoOutput(sessao) -> dict:
        return {
            'id_sessao': sessao.id_sessao,
            'data_hora': sessao.data_hora.isoformat(),
            'filme': {
                'id_filme': sessao.filme.id_filme,
                'titulo': sessao.filme.titulo
            },
            'sala': {
                'id_sala': sessao.sala.id_sala,
                'numero_sala': sessao.sala.numero_sala
            }
        }