from .users import users_bp
from .departament import departament_bp
from .homeSoport import hsoprt_bp
from .devices import devices_bp
from .position import position_bp
from .edith import edith_bp
from .assignment import assignment_bp
from .exportDevices import export_bp
from .importDevices import import_bp
from .verify import verify_bp

def init_app(app):
    app.register_blueprint(users_bp, url_prefix='/user')
    app.register_blueprint(departament_bp, url_prefix='/departament')
    app.register_blueprint(hsoprt_bp, url_prefix='/home')
    app.register_blueprint(position_bp,url_prefix='/posi')
    app.register_blueprint(devices_bp,url_prefix='/devi')
    app.register_blueprint(edith_bp,url_prefix='/edi')
    app.register_blueprint(assignment_bp,url_prefix='/add')
    app.register_blueprint(export_bp,url_prefix='/exp')
    app.register_blueprint(import_bp,url_prefix='/imp')
    app.register_blueprint(verify_bp,url_prefix='/very')

    