from models import db
from flask_login import UserMixin

class User(db.Model, UserMixin):  
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    idDocument = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    rol = db.Column(db.String(20), nullable=False)
    _is_active = db.Column("is_active", db.Boolean, default=True)

    # Relación con Departament por ID
    departament_id = db.Column(db.Integer, db.ForeignKey('departaments.id', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)

    # Relación con Position por ID
    position_id = db.Column(db.Integer, db.ForeignKey('positions.id', onupdate='CASCADE', ondelete='SET NULL'), nullable=True)

    # Relación opcional con Device por 'serial'
    device_serial = db.Column(db.String(70), db.ForeignKey('devices.device_serial'), unique=True, nullable=True)

    def is_active(self):
        return self._is_active  

    def __init__(self, username, fullname, password, idDocument, email, rol, departament_id=None, position_id=None, device_serial=None, is_active=True):
        self.username = username
        self.fullname = fullname
        self.password = password
        self.idDocument = idDocument
        self.email = email
        self.rol = rol
        self.departament_id = departament_id
        self.position_id = position_id
        self.device_serial = device_serial
        self._is_active = is_active

    def __repr__(self):
        return f'<User {self.username}>'




