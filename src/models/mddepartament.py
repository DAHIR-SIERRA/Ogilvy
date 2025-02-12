from models import db

# Modelo de Departamentos
class Departament(db.Model):
    __tablename__ = 'departaments'  # Nombre de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    namedepartament = db.Column(db.String(100), nullable=True, unique=True)

    # Relación con User (departamento puede tener muchos usuarios)
    users = db.relationship('User', backref='departament', lazy=True)

    def __init__(self, namedepartament):
        self.namedepartament = namedepartament

    def __repr__(self):
        return f'<Departament {self.namedepartament}>'
