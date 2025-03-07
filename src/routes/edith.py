from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.mdusers import User,db
from models.mddepartament import Departament
from models.mdposition import Position
from models.mddevices import Device



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
            "serie": device.serie,
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




            
@edith_bp.route('/update_device', methods=['GET', 'POST'])
@login_required
def update_device():
    if current_user.rol !='Admin':
        flash("Accseso denegado","error")
        return redirect(url_for('homeSoport.homeUser'))
    if request.method=='POST':
        id = request.form['id']
        device_serial = request.form['device_serial']
        brand = request.form['brand']
        charger = request.form['charger']
        model = request.form['model']
        activo = request.form['activo']
        serie = request.form['serie']
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

        device_v = Device.query.filter_by(id = id).first()


        if device_v:
            device_v.brand = brand
            device_v.charger = charger
            device_v.model = model
            device_v.device_serial = device_serial
            device_v.activo = activo
            device_v.serie = serie
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
            db.session.commit()
            flash("Dispositivo actualizado correctamente", "success")
            return redirect(url_for('homeSoport.view_devices'))


    return render_template("devices/edith_devices.html")
