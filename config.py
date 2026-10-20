import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuración base de la aplicación PortLife."""
    
    # Clave secreta para sesiones y protección criptográfica
    SECRET_KEY = os.environ.get('SECRET_KEY', 'portlife-cyber-secret-key-2026-unihash-xyz')
    
    # Manejo de Base de Datos: SQLite por defecto, PostgreSQL para producción
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Corrección requerida por Render / Heroku para SQLAlchemy (postgres:// -> postgresql://)
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # SQLite local para desarrollo
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'portlife.db')}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Duración de sesión de administrador
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Credenciales iniciales para el administrador por defecto
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@portlife.dev')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
