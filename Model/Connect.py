from Model.Filme import Filme, Genero, FilmeGenero
from Model.Sessao import Sessao
from Model.BaseModel import db
from Model.Sala import Sala

def initializeDB():
    try:
        db.connect()
        db.create_tables([Filme, Sala, Sessao, Genero, FilmeGenero], safe=True)
    finally:
        db.close()