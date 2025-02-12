from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mddepartament import db, Departament

departament_bp = Blueprint("departament", __name__)

@departament_bp.route('/departaments', methods=['GET', 'POST'])
def departament():
    if request.method == 'POST': 
        namedepartament = request.form['namedepartaments'].strip()  # Elimina espacios en blanco
        
        # Verificar si el departamento ya existe
        existing_departament = Departament.query.filter_by(namedepartament=namedepartament).first()
        
        if existing_departament:
            flash("Este departamento ya existe", "error")
        else:
            newdepartament = Departament(namedepartament=namedepartament)
            db.session.add(newdepartament)
            db.session.commit()
            flash("Registro exitoso", "success")
        
        return redirect(url_for('departament.departament'))  # Evitar reenvío de formularios

    # Obtener todos los departamentos de la base de datos
    departamentos = Departament.query.all()
    return render_template("departaments.html", departamentos=departamentos)


@departament_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    departamento = Departament.query.get(id)
    if departamento:
        db.session.delete(departamento)
        db.session.commit()
        flash("Departamento eliminado correctamente", "success")
    else:
        flash("Departamento no encontrado", "error")
    
    return redirect(url_for('departament.departament'))

@departament_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    departamento = Departament.query.get(id)
    
    if request.method == 'POST':
        # Obtener los nuevos datos del formulario
        namedepartament = request.form['departamentr']
        
        # Actualizar los campos del departamento
        if departamento:
            departamento.namedepartament = namedepartament
            db.session.commit()
            flash("Departamento actualizado correctamente", "success")
            return redirect(url_for('departament.departament'))  # Redirige a la lista de departamentos
        else:
            flash("Departamento no encontrado", "error")
            return redirect(url_for('departament.departament'))
    
    # Si es un GET, prellenar el formulario con los datos actuales
    if departamento:
        return render_template("update_departament.html", departamento=departamento)
    else:
        flash("Departamento no encontrado", "error")
        return redirect(url_for('departament.departament'))



