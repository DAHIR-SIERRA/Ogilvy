import os

DB_USER = "root"      # Cambia esto por el usuario de tu BD
DB_PASSWORD = "123456789"  # Cambia esto por tu contraseña
DB_HOST = "localhost"        # Si usas XAMPP o MariaDB local
DB_NAME = "Base"    # Nombre de tu base de datos en HeidiSQL

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
