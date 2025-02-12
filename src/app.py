from flask import Flask, redirect, url_for
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db  
from models.mdusers import User  
from models.mddevices import Device  
from routes import init_app
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kachy7070'

# Configuración de la BD
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

# Inicializar BD con la app
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"  # Definir la vista de login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Cargar el usuario por ID

# Registrar Blueprints
init_app(app)

@app.route('/')
def index():
    return redirect(url_for('user.login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(host='0.0.0.0', port=5000, debug=True)
