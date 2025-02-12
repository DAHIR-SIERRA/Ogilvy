from models import db


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(30), nullable=False)
    charger = db.Column(db.String(20), nullable=False)
    serial = db.Column(db.String(70), nullable=False, unique=True)
    model = db.Column(db.String(50), nullable=False)
    activo= db.Column(db.String(30), nullable= False, unique= True)
    serie= db.Column(db.String(30), nullable= False, unique= True)
    processor = db.Column(db.String(30), nullable= False, unique= True)
    RAM = db.Column(db.String(15),nullable=False)
    hard_disk= db.Column(db.String(30),nullable=False)
    type_equipement = db.Column(db.String(30),nullable=False)
    keyboard= db.Column(db.String(10),nullable=True)
    mouse= db.Co


    observations = db.Column(db.String(300), nullable=False)
    state = db.Column(db.String(30), nullable=False, default="Not_used")

    # Relación con User (un dispositivo puede estar asignado a un solo usuario)
    user = db.relationship('User', backref='device', lazy=True, uselist=False)

    def __init__(self, brand, charger, serial, model, observations, state="Not_used"):
        self.brand = brand
        self.charger = charger
        self.serial = serial
        self.model = model
        self.observations = observations
        self.state = state

    def assign_to_user(self, user):
        """ Asigna un dispositivo a un usuario y cambia su estado a 'assigned' """
        user.device_serial = self.serial
        self.state = "assigned"

    def unassign(self, user):
        """ Libera el dispositivo y lo marca como disponible """
        user.device_serial = None
        self.state = "Used"
    
    def __repr__(self):
        return f'<Device {self.brand}>'