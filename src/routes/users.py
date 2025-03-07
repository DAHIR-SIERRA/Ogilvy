from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mdusers import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.mddepartament import Departament
from models.mdposition import Position
from models.mddevices import Device

users_bp = Blueprint("user", __name__)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']
        idDocument = request.form['idDocument']
        email = request.form['email']
        rol = 'User'  # Asignar un rol por defecto
        departament_id = request.form['departament']  # Aquí recibes el ID, no el nombre
        position_id = request.form['position']  # Aquí recibes el ID, no el nombre

        # Verificar si el usuario ya existe
        existing_user = User.query.filter(
            (User.username == username) |
            (User.fullname == fullname) |
            (User.email == email) | 
            (User.idDocument == idDocument)
        ).first()

        if existing_user:
            flash("Este usuario ya existe", "error")
            return redirect(url_for('user.register'))

        # Verificar que el departamento existe usando el ID
        departamento = Departament.query.get(departament_id)
        if not departamento:
            flash('El departamento seleccionado no es válido', 'error')
            return redirect(url_for('user.register'))

        # Verificar que la posición existe usando el ID
        posicion = Position.query.get(position_id)
        if not posicion:
            flash('La posición seleccionada no es válida', 'error')
            return redirect(url_for('user.register'))

        # Crear el usuario con los IDs correctos
        new_user = User(
            username=username,
            fullname=fullname,
            password=generate_password_hash(password),
            idDocument=idDocument,
            email=email,
            departament_id=departamento.id,  # Guardar el ID correcto
            position_id=posicion.id,  # Guardar el ID correcto
            rol=rol
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('user.login'))

    # Obtener departamentos y posiciones
    departaments = Departament.query.all()
    carposition = Position.query.all()

    return render_template('auth/register.html', departaments=departaments, cargar_position=carposition)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            
            if user.rol == 'User':
                return redirect(url_for('homeSoport.homeUser'))
            if user.rol == 'Admin':
                return redirect(url_for('homeSoport.home'))
            else:
                flash("Usuario no encontrado")
                return redirect(url_for('user.login'))
        else:
            flash("Credenciales incorrectas", "error")

    return render_template("auth/login.html")

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('user.login'))

@users_bp.route('/home')
@login_required
def home():
    return render_template("homeSoport.html", user=current_user)


@users_bp.route('/assignment', methods=['GET', 'POST'])
@login_required
def assignment():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        id_document = request.form.get('idDocument')
        observations = request.form.get('observations', '')

        user = User.query.filter_by(idDocument=id_document).first()
        if not user:
            flash("Error: Usuario no encontrado.", "error")
            return redirect(url_for('user.assignment'))

        if action == "assign":
            rol = request.form['rol']
            serial = request.form.get('serial', None)
            state = 'Assigned'

            if user.rol != rol:
                user.rol = rol
                db.session.commit()
                flash("Rol actualizado correctamente", "success")
                return redirect(url_for('user.assignment'))

            if serial:
                device = Device.query.filter_by(device_serial=serial).first()
                
                if not device:
                    flash("Error: El dispositivo seleccionado no existe.", "error")
                    return redirect(url_for('user.assignment'))

                if observations:
                    device.observations = observations
                    db.session.commit()
                    flash("Observación registrada", "success")

                if device.state not in ["Not_used", "Deallocated"]:
                    return redirect(url_for('user.assignment'))

                user.device_serial = serial
                device.state = state
                device.observations = observations

            db.session.commit()
            flash("Asignación realizada correctamente.", "success")

        elif action == "delete":
            if user.device_serial:
                device = Device.query.filter_by(device_serial=user.device_serial).first()
                if device:
                    device.state = "Deallocated"
                    device.observations = observations

                user.device_serial = None

            db.session.commit()
            flash("Desasignación realizada correctamente", "success")

        return redirect(url_for('user.assignment'))

    # 🔹 **Consulta mejorada para obtener el nombre del departamento y la posición**
    get_keys = (
        db.session.query(User, Departament.named, Position.namep)
        .outerjoin(Departament, User.departament_id == Departament.id)
        .outerjoin(Position, User.position_id == Position.id)
        .all()
    )

    get_users = User.query.all()
    get_serials = Device.query.filter(Device.state.in_(["Not_used", "Deallocated"])).all()

    get_serials = Device.query.filter(Device.state.in_(["Not_used", "Deallocated"])).all()
    
    return render_template('assignment.html', get_key=get_keys, get_all_serials=get_serials,get_all_users=get_users)




@users_bp.route('/view_serial', methods=['GET', 'POST'])
@login_required
def view_serial():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method== 'POST':
        serial= request.form['serial']

        if not serial or serial == 'None':
            flash("Error este Usuario no tiene asignado un dispositivo","error")
            return redirect(url_for('user.assignment'))
        
        existing_device= Device.query.filter_by(device_serial=serial).first()

        if not existing_device:
            flash("error este serial no existe en la base","error")
            return redirect(url_for('user.assignment'))
            
        
        get_device= {
            "id": existing_device.id,
            "brand":existing_device.brand,
            "charger":existing_device.charger,
            "device_serial": existing_device.device_serial,
            "model":existing_device.model,
            "activo":existing_device.activo,
            "serie": existing_device.serie,
            "processor": existing_device.processor,
            "RAM": existing_device.RAM,
            "hard_disk":existing_device.hard_disk,
            "type_equipment":existing_device.type_equipment,
            "keyboard":existing_device.keyboard,
            "mouse":existing_device.mouse,
            "active_tablet":existing_device.active_tablet,
            "serial_tablet":existing_device.serial_tablet,
            "base":existing_device.base,
            "multi_adapter":existing_device.multi_adapter,
            "screen": existing_device.screen,
            "observations":existing_device.observations,
            "state":existing_device.state
            }


        return render_template("devices/view_serial.html", get_device=get_device)
    
    return render_template("devices/view_serial.html")

       
        