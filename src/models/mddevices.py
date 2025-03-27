from models import db


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(200), nullable=True)
    charger = db.Column(db.String(200), nullable=True)
    device_serial = db.Column(db.String(200), nullable=True, unique=True)
    model = db.Column(db.String(200), nullable=True)
    activo= db.Column(db.String(200), nullable= True,)
    processor = db.Column(db.String(200), nullable= True,)
    RAM = db.Column(db.String(200),nullable=True)
    hard_disk= db.Column(db.String(200),nullable=True)
    type_equipment = db.Column(db.String(200),nullable=True)
    keyboard= db.Column(db.String(200),nullable=True)
    mouse= db.Column(db.String(200),nullable=True)
    active_tablet= db.Column(db.String(200),nullable=True)
    serial_tablet =db.Column(db.String(300),nullable= True, unique = False)
    base = db.Column(db.String(300), nullable=True)
    multi_adapter = db.Column(db.String(300), nullable=True)
    screen = db.Column(db.String(400), nullable=True)
    observations = db.Column(db.String(300), nullable=True)
    old_onwer = db.Column(db.String(300),nullable=True)
    img = db.Column(db.String(600), nullable=True)
    state = db.Column(db.String(30), nullable=True, default="Not_used")
    
    # Relación con User (un dispositivo puede estar asignado a un solo usuario)
    user = db.relationship('User', backref='device', lazy=True, uselist=False)

    def __init__(self, brand, charger, device_serial, model, activo,processor,RAM,hard_disk,type_equipment,
                 keyboard,mouse,active_tablet,serial_tablet,base,multi_adapter,screen,observations,old_onwer, img,state="Not_used"):
        self.brand = brand
        self.charger = charger
        self.device_serial = device_serial
        self.model = model
        self.activo = activo
        self.processor = processor
        self.RAM = RAM
        self.hard_disk = hard_disk
        self.type_equipment = type_equipment
        self.keyboard = keyboard
        self.mouse = mouse
        self.active_tablet = active_tablet
        self.serial_tablet= serial_tablet
        self.base = base
        self.multi_adapter=multi_adapter
        self.screen = screen
        self.observations = observations
        self.old_onwer = old_onwer
        self.img = img
        self.state = state
        

    def __repr__(self):
        return f'<Device {self.brand}>'