from peewee import SqliteDatabase, Model
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, '..', 'Data', 'cinema.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db