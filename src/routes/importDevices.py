from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mddevices import db, Device
import pandas as pd
import os

import_bp = Blueprint('imp', __name__)

@import_bp.route('/import_excel', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        flash('No se encontró el archivo', 'error')
        return redirect(request.referrer)

    file = request.files['file']

    if file.filename == '':
        flash('Nombre de archivo vacío', 'error')
        return redirect(request.referrer)

    try:
        # Verificar la extensión del archivo
        if file.filename.endswith('.xls'):
            df = pd.read_excel(file, engine='xlrd')  # Para archivos .xls
        else:
            df = pd.read_excel(file, engine='openpyxl')  # Para archivos .xlsx

        # Recorrer las filas del DataFrame e insertar en la base de datos
        for _, row in df.iterrows():
            new_device = Device(
                brand=row['brand'],
                charger=row['charger'],
                device_serial=row['device_serial'],
                model=row['model'],
                activo=row['activo'],
                serie=row['serie'],
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
                state=row['state'],
                old_onwer='' if pd.isna(row.get('Old Owner')) else row.get('Old Owner'),
                img=row['img'],
                observations=row['observations']
                 
            )
            db.session.add(new_device)

        db.session.commit()
        flash('Archivo importado con éxito', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al importar el archivo: {str(e)}', 'error')

    return redirect(request.referrer)
