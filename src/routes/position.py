from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mdposition import db, Position
from flask_login import login_required, current_user


position_bp = Blueprint("posi",__name__)


@position_bp.route('/position', methods=['GET', 'POST'])
@login_required
def position():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method == 'POST': 
        nameposition = request.form['nameposition'].strip()  # Elimina espacios en blanco
        
        # Verificar si la position ya existe
        existing_position = Position.query.filter_by(namep=nameposition).first()
        
        if existing_position:
            flash("Esta posicion ya existe", "error")
        else:
            newposition= Position(namep=nameposition)
            db.session.add(newposition)
            db.session.commit()
            flash("Registro exitoso", "success")
        
        return redirect(url_for('posi.position'))  # Evitar reenvío de formularios

    # Obtener todos los posiciones de la base de datos
    positioncarg = Position.query.all()
    return render_template("Home/homesoport/position/position.html", position_cargada=positioncarg)


@position_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    position = Position.query.get(id)

    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method == 'POST':
        # Obtener los nuevos datos del formulario
        newposition = request.form['positionr']
        
        # Actualizar los campos del la posicion
        if newposition:
            position.namep = newposition
            db.session.commit()
            flash("Posicion actualizado correctamente", "success")
            return redirect(url_for('posi.position'))  # Redirige a la lista de posicion
        else:
            flash("Posicion no encontrado", "error")
            return redirect(url_for('posi.position'))
    
   
    else:
        flash("Posicion no encontrado", "error")
        return redirect(url_for('posi.position'))
    

@position_bp.route('/deleted/<int:id>', methods=['POST'])
@login_required
def deleted(id):
    position = Position.query.get(id)
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if position:
        db.session.delete(position)
        db.session.commit()
        flash("Posicion eliminado correctamente", "success")
    else:
        flash("Posicion no encontrado", "error")
    
    return redirect(url_for('posi.position'))



    



