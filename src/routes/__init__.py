from .users import users_bp
from .departament import departament_bp
from .homeSoport import hsoprt_bp
from .devices import devices_bp

def init_app(app):
    app.register_blueprint(users_bp, url_prefix='/user')
    app.register_blueprint(departament_bp, url_prefix='/departament')
    app.register_blueprint(hsoprt_bp, url_prefix='/home')
    app.register_blueprint(devices_bp,url_prefix='/view')