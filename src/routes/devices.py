from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from models import Device, db
from flask_login import login_required, current_user
import os
import uuid  # Para generar nombres únicos en las imágenes
from werkzeug.utils import secure_filename

# Configuración del directorio donde se guardarán las imágenes
UPLOAD_FOLDER = 'src/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar que la carpeta de subida existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

devices_bp = Blueprint('devi', __name__)

# Función para validar extensiones de archivo permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@devices_bp.route('/devices', methods=['GET', 'POST'])
@login_required
def devices():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))

    if request.method == 'POST':
        brand = request.form['brand']
        charger = request.form['charger']
        device_serial = request.form['device_serial']
        model = request.form['model']
        activo = request.form['activo']
        serie = request.form['serie']
        processor = request.form['processor']
        ram = request.form['ram']
        hard_disk = request.form['hard_disk']
        type_equipment = request.form['type_equipment']
        keyboard = request.form['keyboard']
        mouse = request.form['mouse']
        active_tablet = request.form['active_tablet']
        serial_tablet = request.form['serial_tablet']
        base = request.form['base']
        multi_adapter = request.form['multi_adapter']
        screen = request.form['screen']
        state = 'Not_used'
        observations = request.form['observations']

        # Verificar si ya existe un dispositivo con datos únicos
        if Device.query.filter_by(device_serial=device_serial).first() or \
           Device.query.filter_by(activo=activo).first() or \
           Device.query.filter_by(screen=screen).first() or \
           Device.query.filter_by(serie=serie).first():
            flash("Este dispositivo ya existe", "error")
            return redirect(url_for('devi.devices'))

        # Manejo de subida de imagen
        image_file = request.files.get('img')
        img_path = None  # Inicializar la variable de imagen

        if image_file and allowed_file(image_file.filename):
            # Generar un nombre único para evitar sobrescribir imágenes
            ext = image_file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            img_path = f"uploads/{filename}"  # Ruta relativa
            image_file.save(os.path.join(UPLOAD_FOLDER, filename))  # Guardar la imagen

        # Crear y guardar el nuevo dispositivo
        new_device = Device(
            brand=brand,
            charger=charger,
            device_serial=device_serial,
            model=model,
            activo=activo,
            serie=serie,
            processor=processor,
            RAM=ram,
            hard_disk=hard_disk,
            type_equipment=type_equipment,
            keyboard=keyboard,
            mouse=mouse,
            active_tablet=active_tablet,
            serial_tablet=serial_tablet,
            base=base,
            multi_adapter=multi_adapter,
            screen=screen,
            observations=observations,
            old_onwer='None',
            img=img_path,  # Guardar solo la ruta relativa
            state=state
        )

        db.session.add(new_device)
        db.session.commit()
        flash("Dispositivo registrado", "success")
        return redirect(url_for('devi.devices'))

    return render_template('devices/devices.html')
