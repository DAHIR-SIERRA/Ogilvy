from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.mdusers import User,db
from models.mddepartament import Departament
from models.mdposition import Position
from models.mddevices import Device

hsoprt_bp = Blueprint('homeSoport', __name__)

@hsoprt_bp.route('/homeSoport', methods=['GET', 'POST'])
@login_required
def home():
    
    
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    else:
     cont_devices= Device.query.count()
     cont_maintenance = Device.query.filter_by(state ='maintenance').count()
     cont_deallocated = Device.query.filter_by(state='deallocated').count()
     cont_not_used = Device.query.filter_by(state='Not_used').count()
     cont_assigned = Device.query.filter_by(state='Assigned').count()
            
        


    
    
    return render_template('homeSoport.html',user=current_user,
                           cont_devices=cont_devices,
                           cont_maintenance=cont_maintenance,
                           cont_deallocated=cont_deallocated,
                           cont_assigned = cont_assigned,
                           cont_not_used=cont_not_used)




@hsoprt_bp.route('/homeUser', methods=['GET', 'POST'])
@login_required
def homeUser():
    if current_user.rol != "User":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.home'))
    else:
        get_keys = (
        db.session.query(User, Departament.named, Position.namep)
        .outerjoin(Departament, User.departament_id == Departament.id)
        .outerjoin(Position, User.position_id == Position.id)
        .filter(User.id == current_user.id)# Filtra solo el usuario autenticado
        .all()
    )
   
    
    
    return render_template('homeUser.html',user=current_user,get_all_keys=get_keys)

@hsoprt_bp.route('/view_devices', methods=['GET', 'POST'])
@login_required
def view_devices():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    # Obtener todos los dispositivos por defecto
    get_devices = Device.query.all()

    # Si se envía un formulario con una categoría seleccionada
    selected_category = request.form.get("selected_category")
    if selected_category:
        if selected_category == 'Total Devices':
            return render_template('devices/view_devices.html', get_devices=get_devices)
        flash("Categoría no encontrada", "error")
        return redirect(url_for('homeSoport.view_devices'))

    # Renderiza la vista con todos los dispositivos por defecto
    return render_template('devices/view_devices.html', get_devices=get_devices)



