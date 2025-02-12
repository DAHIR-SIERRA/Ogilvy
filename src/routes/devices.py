from flask import Flask, render_template, request, redirect, url_for, flash,Blueprint

devices_bp = Blueprint('devices',__name__)


@devices_bp.route('/devices', methods=['GET', 'POST'])
def devices():
    return render_template("devices.html")
