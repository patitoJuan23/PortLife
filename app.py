import os
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv

from config import Config
from models import db, User, Profile
from seed import seed_database
from routes.public import public_bp
from routes.admin import admin_bp

# Cargar variables de entorno si existe archivo .env
load_dotenv()

def create_app(config_class=Config):
    """Fábrica de la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar Base de Datos
    db.init_app(app)

    # Inicializar Gestor de Sesiones de Administrador
    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Por favor inicia sesión con tu cuenta de administrador para acceder a este panel.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Inyección de variables globales a todas las plantillas Jinja2
    @app.context_processor
    def inject_global_vars():
        profile = Profile.query.first()
        return {
            'site_profile': profile,
            'current_year': datetime.now().year,
            'app_name': 'PortLife'
        }

    # Registro de Blueprints (Rutas públicas y administrativas)
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # Manejo de Errores HTTP
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # Comandos CLI para gestión administrativa y despliegue
    @app.cli.command('init-db')
    def init_db_command():
        """Inicializa las tablas y datos semilla."""
        seed_database(app)
        print("Base de datos de PortLife inicializada exitosamente.")

    @app.cli.command('create-admin')
    def create_admin_command():
        """Crea o actualiza el usuario administrador desde variables de entorno."""
        with app.app_context():
            u = app.config.get('ADMIN_USERNAME', 'admin')
            p = app.config.get('ADMIN_PASSWORD', 'admin123')
            e = app.config.get('ADMIN_EMAIL', 'admin@portlife.dev')

            user = User.query.filter_by(username=u).first()
            if not user:
                user = User(username=u, email=e)
                user.set_password(p)
                db.session.add(user)
                print(f"Administrador '{u}' creado.")
            else:
                user.set_password(p)
                print(f"Contraseña de administrador '{u}' actualizada.")
            db.session.commit()

    # Inicialización automática de la base de datos y datos semilla en el primer arranque
    with app.app_context():
        seed_database(app)

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
