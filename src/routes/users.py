from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.mdusers import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask import session
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
        departament_id = request.form['departament'] 
        position_id = request.form['position']  

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
    logout_user()  # Cierra la sesión con Flask-Login
    session.clear()  # Borra toda la información de la sesión
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('user.login'))


@users_bp.route('/home')
@login_required
def home():
    return render_template("homeSoport.html", user=current_user)


    
@users_bp.route('/verify_edith', methods=['GET', 'POST'])
@login_required
def verify_edith():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))
    
    if request.method == 'POST':
        code_edith = request.form.get('code_edith')  # Usa .get() para evitar errores si no existe
        user = User.query.filter_by(code_edith=code_edith).first()  # Asegura que solo devuelve un usuario

        if user:
            departaments = Departament.query.all()
            carposition = Position.query.all()
            flash("Usuario encontrado", "success")
            return render_template('users.html', user=user, departaments=departaments, carposition=carposition)  # Pasar el usuario encontrado a la plantilla
        else:
            flash("Usuario no ha sido encontrado o el código ha sido desactivado", "error")

    return render_template('verify_code.html')  # Siempre renderiza la página en GET

         
@users_bp.route('/users', methods=['GET', 'POST'])
def users():
    if current_user.rol != "Admin":
        flash("Acceso denegado", "error")
        return redirect(url_for('homeSoport.homeUser'))


    if request.method == 'POST':
        user_id = request.form.get("id")
        username = request.form.get("username")
        fullname = request.form.get("fullname")
        id_document = request.form.get("idDocument")
        role = request.form.get("rol")
        departament_id = request.form.get("departament_id")
        position_id = request.form.get("position_id")

        # Buscar usuario en la base de datos
        user = User.query.get(user_id)
        if not user:
            flash("Usuario no encontrado", "error")
            return redirect(url_for("user.verify_edith"))

        # Actualizar datos del usuario
        user.username = username
        user.fullname = fullname
        user.idDocument = id_document
        user.rol = role
        user.departament_id = departament_id
        user.position_id = position_id

        # Guardar cambios en la base de datos
        try:
            db.session.commit()
            flash("Usuario actualizado correctamente", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar usuario: {str(e)}", "error")

        return redirect(url_for("user.verify_edith"))

    return render_template("users.html")

         

         




       
        