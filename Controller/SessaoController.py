from Controller.FilmeController import FilmeController
from Controller.SalaController import SalaController
from peewee import DoesNotExist
from Model.Sessao import Sessao
from Model.Filme import Filme
from Model.Sala import Sala
from datetime import datetime

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
            raise ValueError(f"Erro ao criar uma sessão: {str(e)}")

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
            raise ValueError(f"Error ao ler as sessões: {str(e)}")

    @staticmethod
    def readById(id_sessao):
        try:
            sessao = (Sessao
                    .select(Sessao, Filme, Sala)
                    .join(Filme, on=(Sessao.filme == Filme.id_filme))
                    .join(Sala, on=(Sessao.sala == Sala.id_sala))
                    .where(Sessao.id_sessao == id_sessao)
                    .get())

            return sessao
        except DoesNotExist:
            raise ValueError(f"Sessão com ID {id_sessao} não encontrada")
        except Exception as e:
            raise ValueError("Erro ao buscar dados da sessão")

    @staticmethod
    def readByData(data=None):
        return Sessao.readByDate(data)

    @staticmethod
    def update(id_sessao, **kwargs):
        try:
            if 'data_hora' in kwargs:
                try:
                    kwargs['data_hora'] = datetime.fromisoformat(kwargs['data_hora'])
                except ValueError:
                    raise ValueError("Formato de data/hora inválido. Use o formato (YYYY-MM-DDTHH:MM:SS)")

            return Sessao.update(id_sessao, **kwargs)

        except DoesNotExist as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")

    @staticmethod
    def delete(id_sessao=int):
        try:
            deleted_count = Sessao.delete(id_sessao)
            return deleted_count > 0
        except DoesNotExist as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")

    @staticmethod
    def _formatSessaoOutput(sessao):
        
        if isinstance(sessao.data_hora, str):
            try:
                if "+" in sessao.data_hora:
                    sessao.data_hora = datetime.strptime(
                        sessao.data_hora.split("+")[0].strip(),
                        "%Y-%m-%d %H:%M:%S"
                    )
                else:
                    sessao.data_hora = datetime.strptime(sessao.data_hora, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                raise ValueError(f"Formato de data/hora inválido: {sessao.data_hora}") from e

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