from models import db

class Departament(db.Model):
    __tablename__ = 'departaments'  # Nombre de la tabla en la BD

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    named = db.Column(db.String(100), nullable=False, unique=True)

    # Relación con User (departamento puede tener muchos usuarios)
    users = db.relationship('User', backref='departament', passive_deletes=True)


    def __init__(self, named):
        self.named = named

    def __repr__(self):
        return f'<Departament {self.named}>'
