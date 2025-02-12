from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar modelos para que SQLAlchemy los registre
from .mddevices import Device
from .mdusers import User
from .mddepartament import Departament

def init_app(app):
    db.init_app(app)
