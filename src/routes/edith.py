from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.mdusers import User,db
from models.mddepartament import Departament
from models.mdposition import Position
from models.mddevices import Device
from werkzeug.utils import secure_filename
import os
import uuid

# Configuración del directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'src/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar que la carpeta de subida existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

devices_bp = Blueprint('devi', __name__)

# Función para validar extensiones de archivo permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



edith_bp= Blueprint('edi',__name__)

@edith_bp.route('/edith_devices', methods=['GET', 'POST'])
@login_required
def edith_devices():
    if current_user.rol != 'Admin':
        flash("Acceso denegado", "error")
        return redirect(url_for('edi.edith_devices'))

    if request.method == 'POST':
        device_id = request.form.get('device_id')  # Usar .get() evita KeyError si el campo falta
        if not device_id:
            flash("Debe ingresar un ID de dispositivo", "error")
            return redirect(url_for('edi.edith_devices'))

        device = Device.query.filter_by(id=device_id).first()
        if not device:
            flash("Dispositivo no encontrado", "error")
            return redirect(url_for('edi.edith_devices'))

        get_device = {
            "id": device.id,
            "brand": device.brand,
            "charger": device.charger,
            "device_serial": device.device_serial,
            "model": device.model,
            "activo": device.activo,
            "processor": device.processor,
            "RAM": device.RAM,
            "hard_disk": device.hard_disk,
            "type_equipment": device.type_equipment,
            "keyboard": device.keyboard,
            "mouse": device.mouse,
            "active_tablet": device.active_tablet,
            "serial_tablet": device.serial_tablet,
            "base": device.base,
            "multi_adapter": device.multi_adapter,
            "screen": device.screen,
            "observations": device.observations,
            "state": device.state
        }
        

        return render_template("devices/edith_devices.html", get_device=get_device)

    return render_template("devices/edith_devices.html")




@edith_bp.route('/update_device', methods=['POST'])
@login_required
def update_device():
    if current_user.rol != 'Admin':
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))

    # Obtener datos del formulario usando request.form[]
    id = request.form['id']

    brand = request.form['brand']
    charger = request.form['charger']
    model = request.form['model']
    activo = request.form['activo']
    processor = request.form['processor']
    ram = request.form['RAM']
    hard_disk = request.form['hard_disk']
    type_equipment = request.form['type_equipment']
    keyboard = request.form['keyboard']
    mouse = request.form['mouse']
    active_tablet = request.form['active_tablet']
    serial_tablet = request.form['serial_tablet']
    base = request.form['base']
    multi_adapter = request.form['multi_adapter']
    screen = request.form['screen']
    observations = request.form['observations']

    # Buscar el dispositivo en la base de datos
    device_v = Device.query.filter_by(id=id).first()

    if not device_v:
        flash("Dispositivo no encontrado", "error")
        return redirect(url_for('homeSoport.view_devices'))

    # Manejo de la imagen
    image_file = request.files.get('img')
    if image_file and allowed_file(image_file.filename):
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        img_path = f"uploads/{filename}"
        image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        img_path = device_v.img  # Mantener la imagen anterior

    # Actualizar los datos del dispositivo
    device_v.brand = brand
    device_v.charger = charger
    device_v.model = model
    device_v.activo = activo
    device_v.processor = processor
    device_v.RAM = ram
    device_v.hard_disk = hard_disk
    device_v.type_equipment = type_equipment
    device_v.keyboard = keyboard
    device_v.mouse = mouse
    device_v.active_tablet = active_tablet
    device_v.serial_tablet = serial_tablet
    device_v.base = base
    device_v.multi_adapter = multi_adapter
    device_v.screen = screen
    device_v.observations = observations
    device_v.img = img_path  # Asignar la imagen actualizada

    # Guardar los cambios en la base de datos
    db.session.commit()

    get_devices = Device.query.all()


    flash("Dispositivo actualizado correctamente", "success")
    return render_template('devices/view_devices.html',get_devices = get_devices)

    
@edith_bp.route('devices/maintenance',methods=['GET','POST'])
@login_required
def maintenance():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method=='POST':
        id= request.form['id']
        serial= request.form['serial']
        existing_id = Device.query.filter_by(id = id).first()
        have_owner= User.query.filter_by(device_serial= serial).first()
        if have_owner:
            flash("Antes de enviar este dispositivo a mantenimiento, debes desvincularlo del usuario al que está asignado","error")
            return redirect(url_for('devi.view_devices'))

        if existing_id:
            existing_id.state = 'maintenance'
            db.session.commit()
            flash("El dispositivo entro en mantenimiento","success")
            return redirect(url_for('devi.view_devices'))
        else:
            flash("No fue posdible llevar dispositivo a mantenimiento","error")
    
    return render_template("devices/maintenance.html")

@edith_bp.route('devices/repaired',methods=['GET','POST'])
@login_required
def repaired():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    get_maintenance =Device.query.filter_by(state='maintenance').all()
    
    if request.method=='POST':
        id= request.form['id']
        existing_id = Device.query.filter_by(id = id).first()

        if existing_id:
            existing_id.state = 'Repaired'
            db.session.commit()
            flash("El dispositivo fue reparado","success")
            return redirect(url_for('homeSoport.home'))
        else:
            flash("Dispositivo no dado de alta","error")
    
    return render_template("devices/maintenance.html", get_maintenance=get_maintenance)


