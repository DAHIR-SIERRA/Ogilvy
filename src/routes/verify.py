from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from models.mdusers import db, User
from flask_login import current_user, login_required
from flask_mail import Mail

# Asumiendo que ya tienes configurado Flask-Mail con 'mail'
mail = Mail()

verify_bp = Blueprint("very", __name__)

# Vista para mostrar el formulario de verificación
@verify_bp.route('/verify', methods=['GET', 'POST'])
@login_required  # Aseguramos que el usuario esté autenticado
def verify():
    user = current_user
    return render_template("auth/verify_account.html", user=user)

# Vista para actualizar el email del usuario
@verify_bp.route('/email_update', methods=['POST'])
def update_email():
    email = request.form['email']
    idDocument = request.form['idDocument']

    # Buscar usuario por documento
    user = User.query.filter_by(idDocument=idDocument).first()

    if user:
        user.email = email
        db.session.commit()
        flash("Email actualizado con éxito", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return render_template("auth/verify_account.html", user=user)

# Vista para enviar el correo de verificación
@verify_bp.route("/send_email", methods=["POST"])
def send_email():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()

    if user:
        msg = Message("Verifica tu cuenta", sender="braynerdahirsierrasanabria@gmail.com", recipients=[user.email])
        msg.body = f"Tu código de verificación es: {user.code_edith}"  # Suponiendo que 'code_edith' es el código
        mail.send(msg)
        flash("Correo enviado correctamente", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return redirect(url_for("very.request_code"))

# Vista para ingresar y validar el código de verificación
@verify_bp.route("/request_code", methods=["GET", "POST"])
def request_code():
    if request.method == "POST":
        code = request.form.get("code_of_verify")
        # Validar el código de verificación aquí
        if code == current_user.code_edith:  # Suponiendo que 'code_edith' es el código almacenado
            flash("Código verificado con éxito", "success")
            return redirect(url_for("user.login"))  # Redirige a donde corresponda
        else:
            flash("Código incorrecto. Intenta de nuevo", "danger")
    
    return render_template("auth/inner_code.html")  # Asegúrate de que el formulario esté en este HTML

