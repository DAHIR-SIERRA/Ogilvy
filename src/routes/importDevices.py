from flask import Blueprint, render_template, request, flash, redirect,url_for
from models.mddevices import db, Device
from flask_login import login_required, current_user
import pandas as pd
import numpy as np


import_bp = Blueprint('imp', __name__)

@import_bp.route('/import_excel', methods=['POST'])
@login_required
def import_excel():
     if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
     if 'file' not in request.files:
         flash('No se encontró el archivo', 'error')
         return redirect(request.referrer)

     file = request.files['file']

     if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(request.referrer)

     try:
        # Verificar la extensión del archivo y cargar datos
        if file.filename.endswith('.xls'):
            df = pd.read_excel(file, engine='xlrd')  # Para archivos .xls
        else:
            df = pd.read_excel(file, engine='openpyxl')  # Para archivos .xlsx
        
        # Reemplazar valores NaN con None
        df = df.replace({np.nan: None})

        dispositivos_agregados = 0
        dispositivos_ignorados = 0

        for _, row in df.iterrows():
            # Verificar si el dispositivo ya existe en la base de datos
            existing_device = Device.query.filter(
                (Device.device_serial == row['device_serial']) 
            ).first()

            if existing_device:
                dispositivos_ignorados += 1
                continue  # Saltar este dispositivo y continuar con el siguiente

            # Crear y agregar un nuevo dispositivo si no existe
            new_device = Device(
                brand=row['brand'],
                charger=row['charger'],
                device_serial=row['device_serial'],
                model=row['model'],
                activo=row['activo'],
                processor=row['processor'],
                RAM=row['RAM'],
                hard_disk=row['hard_disk'],
                type_equipment=row['type_equipment'],
                keyboard=row['keyboard'],
                mouse=row['mouse'],
                active_tablet=row['active_tablet'],
                serial_tablet=row['serial_tablet'],
                base=row['base'],
                multi_adapter=row['multi_adapter'],
                screen=row['screen'],
                state='Not_Used',
                old_onwer='' if pd.isna(row.get('Old Owner')) else row.get('Old Owner'),
                img=row['img'],
                observations=row['observations']
            )

            db.session.add(new_device)
            dispositivos_agregados += 1

        # Confirmar los cambios en la base de datos solo si se agregaron dispositivos nuevos
        if dispositivos_agregados > 0:
            db.session.commit()
            flash(f'Se importaron {dispositivos_agregados} dispositivos nuevos.', 'success')
        else:
            flash('No se importaron nuevos dispositivos. Todos los dispositivos ya existen en la base de datos.', 'error')

        if dispositivos_ignorados > 0:
            flash(f'{dispositivos_ignorados} dispositivos ya existían y fueron ignorados.', 'error')

     except Exception as e:
        db.session.rollback()
        flash(f'Error al importar el archivo: {str(e)}', 'error')

     return redirect(request.referrer)
