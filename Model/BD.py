from peewee import SqliteDatabase
from config import Config

db = SqliteDatabase(Config.DATABASE)

def initialize_db():
    db.connect()
    db.create_tables([Filme, Sala, Sessao], safe=True)
    db.close()