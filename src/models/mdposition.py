from models import db

# Modelo de Cargos (Positions)
class Position(db.Model):
    __tablename__ = 'positions'  # Nombre de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namep = db.Column(db.String(100), nullable=False, unique=True)  # Cambié 'position' por 'name' para mayor claridad

    # Relación con User (un cargo puede tener muchos usuarios)
    users = db.relationship('User', backref='position', lazy=True,passive_deletes=True)

    def __init__(self, namep):
        self.namep = namep

    def __repr__(self):
        return f'<Position {self.namep}>'
