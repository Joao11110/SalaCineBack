import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    DATABASE = os.path.join(BASE_DIR, 'data', 'cinema.db')
    DEBUG = True