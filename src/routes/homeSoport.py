from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_required, current_user
from models.mdusers import User,db
from models.mddepartament import Departament
from models.mdposition import Position
from models.mddevices import Device

hsoprt_bp = Blueprint('homeSoport', __name__)

# Ruta para Vista home

@hsoprt_bp.route('/homeSoport', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    else:
     cont_devices= Device.query.filter(Device.state !='maintenance').count()
     cont_maintenance = Device.query.filter_by(state ='maintenance').count()
     cont_users = User.query.count()

            
     return render_template('Home/homesoport/homeSoport.html',user=current_user,
                           cont_all_devices=cont_devices,
                           cont_maintenance=cont_maintenance,
                           cont_users=cont_users)



# Ruta para Vista Home Usuario
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
   
    
    
    return render_template('Home/homeuser/homeUser.html',user=current_user,get_all_keys=get_keys)




@hsoprt_bp.route('/selectd', methods=['GET', 'POST'])
@login_required
def selectd():
        if current_user.rol != "Admin":
            flash("Acceso denegado", "error")
            return redirect(url_for('homeSoport.homeUser'))

        get_devices = Device.query.filter(Device.state != 'maintenance').all()
        get_maintenance =Device.query.filter_by(state='maintenance').all()
        cont_devices= Device.query.filter(Device.state !='maintenance').count()
        cont_maintenance = Device.query.filter_by(state ='maintenance').count()
        cont_users = User.query.count()

        

    # Filtrar por categoría si se seleccionó una
        selected_category = request.form.get("selected_category")
        if selected_category:
            if selected_category == 'Total Devices':
                redirect(url_for('devi.view_devices'))
                return render_template('Home/homesoport/devices/view_devices.html', get_devices=get_devices)
                
            
            if selected_category == 'Maintenance':
                redirect(url_for('edi.maintenance'))
                return render_template('Home/homesoport/maintenance/maintenance.html', get_maintenance=get_maintenance)
            
            if selected_category == 'Users':
                redirect(url_for('user.verify_edith'))
                return render_template('Home/homesoport/edith_user/verify_code.html')
            
            if selected_category =='Export':
                redirect(url_for('export.export_page'))
                return render_template('Home/homesoport/import_and_export/export.html')
            
            return render_template('Home/homesoport/devices/view_devices.html')
        
        return render_template("Home/homesoport/homeSoport.html", get_devices=get_devices,
                            cont_all_devices=cont_devices,
                            cont_maintenance=cont_maintenance,
                            cont_users = cont_users)