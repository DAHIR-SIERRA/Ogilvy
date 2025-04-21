
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
        serial = request.form.get('device_serial')
        observations = request.form.get('observations', '').strip()

        device = Device.query.filter_by(device_serial=serial).first()

        if not device:
            flash("Error: No hay Usuario seleccionado.", "error")
            return redirect(url_for('add.assignment'))

        if action == "assign":

            idDocument = request.form.get('idDocument')

            if idDocument:
                verify_id = User.query.filter_by(idDocument=idDocument).first()

                if not verify_id:
                    flash("Error: El Usuario seleccionado no existe.", "error")
                elif device.state not in ["Not_Used", "Deallocated", "Repaired"]:
                    flash(f"Error: El estado del dispositvo es  {device.state}", "error")
                else:
                    device.user_idDocument = idDocument
                    device.state = "Assigned"
                    device.observations = observations
                    db.session.commit()
                    flash("Asignación realizada correctamente.", "success")
                

        elif action == "delete" and device.user_idDocument:

            device = Device.query.filter_by(user_idDocument= device.user_idDocument).first()


            if device:
                assigned_user = User.query.filter_by(idDocument=device.user_idDocument).first()
                device.state = "Deallocated"
                device.observations = observations
                device.old_onwer = assigned_user.fullname

            device.user_idDocument = None
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
    get_serials = Device.query.all()

    return render_template('Home/homesoport/assignment/assignment.html', get_key=get_keys, get_all_serials=get_serials, get_all_users=get_users)




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
            
        
       

        return render_template("Home/homesoport/devices/view_serial.html", get_device=existing_device)

