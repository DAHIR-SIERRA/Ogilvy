from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mdusers import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.mddepartament import Departament

users_bp = Blueprint("user", __name__)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']
        idDocument = request.form['idDocument']
        email = request.form['email']
        rol = 'user'  # Asignar un rol por defecto
        namedepartament = request.form['departament']

        existing_user = User.query.filter(
            (User.username == username) |
            (User.fullname == fullname) |
            (User.email == email) |
            (User.idDocument == idDocument)
        ).first()

        if existing_user:
            flash("Este usuario ya existe", "error")
            return redirect(url_for('user.register'))
        
        # Verificar que el departamento existe
        departamento = Departament.query.filter_by(namedepartament=namedepartament).first()
        if not departamento:
            flash('El departamento seleccionado no es válido', 'error')
            return redirect(url_for('user.register'))

        new_user = User(
            username=username,
            fullname=fullname,
            password=generate_password_hash(password),
            idDocument=idDocument,
            email=email,
            namedepartament=namedepartament,
            rol=rol
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('user.login'))  # Especifica el Blueprint

    # Obtener todos los departamentos
    departaments = Departament.query.all()
    return render_template('register.html', departaments=departaments)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('homeSoport.home'))  # Asegurar que 'home' es el blueprint correcto
        else:
            flash("Credenciales incorrectas", "error")

    return render_template("login.html")

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
