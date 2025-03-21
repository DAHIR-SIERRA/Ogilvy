
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mdusers import db, User
from flask_login import login_user, logout_user, login_required, current_user
from models.mddepartament import Departament
from models.mdposition import Position
from models.mddevices import Device

assignment_bp = Blueprint("add",__name__)


@assignment_bp.route('/assignment', methods=['GET', 'POST'])
@login_required
def assignment():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))

    if request.method == 'POST':
        action = request.form.get('action')
        id_document = request.form.get('idDocument')
        observations = request.form.get('observations', '').strip()

        user = User.query.filter_by(idDocument=id_document).first()

        if not user:
            flash("Error: Usuario no encontrado.", "error")
            return redirect(url_for('add.assignment'))

        if action == "assign":
            rol = request.form.get('rol')
            serial = request.form.get('serial')

            if user.rol != rol:
                user.rol = rol
                flash("Rol actualizado correctamente", "success")

            if serial:
                device = Device.query.filter_by(device_serial=serial).first()

                if not device:
                    flash("Error: El dispositivo seleccionado no existe.", "error")
                elif device.state not in ["Not_Used", "Deallocated", "Repaired"]:
                    flash("Error: El dispositivo no está disponible para asignación.", "error")
                else:
                    user.device_serial = serial
                    device.state = "Assigned"
                    device.observations = observations
                    flash("Asignación realizada correctamente.", "success")

        elif action == "delete" and user.device_serial:
            device = Device.query.filter_by(device_serial=user.device_serial).first()

            if device:
                device.state = "Deallocated"
                device.observations = observations

            user.device_serial = None
            flash("Desasignación realizada correctamente.", "success")

        db.session.commit()
        return redirect(url_for('add.assignment'))

    # 🔹 **Consulta mejorada para obtener información de usuarios**
    get_keys = (
        db.session.query(User, Departament.named, Position.namep)
        .outerjoin(Departament, User.departament_id == Departament.id)
        .outerjoin(Position, User.position_id == Position.id)
        .all()
    )

    get_users = User.query.all()
    get_serials = Device.query.filter(Device.state.in_(["Not_Used", "Deallocated", "Repaired"])).all()

    return render_template('assignment.html', get_key=get_keys, get_all_serials=get_serials, get_all_users=get_users)




@assignment_bp.route('/view_serial', methods=['GET', 'POST'])
@login_required
def view_serial():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method== 'POST':
        serial= request.form['serial']

        if not serial or serial == 'None':
            flash("Error este Usuario no tiene asignado un dispositivo","error")
            return redirect(url_for('add.assignment'))
        
        existing_device= Device.query.filter_by(device_serial=serial).first()

        if not existing_device:
            flash("error este serial no existe en la base","error")
            return redirect(url_for('add.assignment'))
            
        
       

        return render_template("devices/view_serial.html", get_device=existing_device)

