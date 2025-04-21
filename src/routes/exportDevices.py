from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from models.mddevices import db, Device
from flask_login import login_required, current_user
import xlwt
import io

export_bp = Blueprint('export', __name__)

@export_bp.route('/export_page')
@login_required
def export_page():
     if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
     return render_template('Home/homesoport/import_and_export/export.html')

@export_bp.route('/ajax_export', methods=['GET'])
@login_required
def ajax_export():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    # Crear libro de Excel
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('devices')

    # Salida en memoria
    output = io.BytesIO()

    row_num = 0

    # Encabezados del Excel (coincidiendo con los nombres esperados en la importación)
    columns = [
        'id', 'brand', 'charger', 'device_serial', 'model', 'activo',
        'processor', 'RAM', 'hard_disk', 'type_equipment', 'keyboard', 'mouse',
        'active_tablet', 'serial_tablet', 'base', 'multi_adapter', 'screen',
        'state','old_onwer','img','user_idDocument','observations'
    ]

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    # Obtener los dispositivos de la base de datos
    devices = Device.query.all()

    # Agregar datos al archivo Excel
    for dev in devices:
        row_num += 1
        ws.write(row_num, 0, str(dev.id))
        ws.write(row_num, 1, dev.brand or '')
        ws.write(row_num, 2, dev.charger or '')
        ws.write(row_num, 3, dev.device_serial or '')
        ws.write(row_num, 4, dev.model or '')
        ws.write(row_num, 5, dev.activo or '')
        ws.write(row_num, 6, dev.processor or '')
        ws.write(row_num, 7, dev.RAM or '')
        ws.write(row_num, 8, dev.hard_disk or '')
        ws.write(row_num, 9, dev.type_equipment or '')
        ws.write(row_num, 10, dev.keyboard or '')
        ws.write(row_num, 11, dev.mouse or '')
        ws.write(row_num, 12, dev.active_tablet or '')
        ws.write(row_num, 13, dev.serial_tablet or '')
        ws.write(row_num, 14, dev.base or '')
        ws.write(row_num, 15, dev.multi_adapter or '')
        ws.write(row_num, 16, dev.screen or '')
        ws.write(row_num, 17, dev.state or '')
        ws.write(row_num, 18, dev.old_onwer or '')
        ws.write(row_num, 19, dev.img or '')
        ws.write(row_num, 20, dev.user_idDocument or '')
        ws.write(row_num, 21, dev.observations or '')
        

    # Guardar en la salida
    wb.save(output)
    output.seek(0)

    # Configurar encabezados de respuesta
    response_header = {
        'Content-Disposition': 'attachment; filename=Devices.xls'
    }

    # Retornar el archivo como respuesta
    return Response(output.getvalue(), mimetype="application/vnd.ms-excel", headers=response_header)