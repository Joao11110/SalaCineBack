from Model.Filme import Filme, Genero, FilmeGenero
from Model.Sala import Sala
from Model.Sessao import Sessao
from Model.BaseModel import db

def initialize_db():
    try:
        db.connect()
        db.create_tables([Filme, Sala, Sessao, Genero, FilmeGenero], safe=True)
    finally:
        db.close()