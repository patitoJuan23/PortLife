from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    """Modelo para usuarios administradores y registrados del sistema."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="admin")  # 'admin' o 'user'
    full_name = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def set_password(self, password):
        """Genera un hash seguro para la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Valida una contraseña contra su hash."""
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.username == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    """Información personal y académica del estudiante."""
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False, default="Juan Miguel Duarte Castañeda")
    document_id = db.Column(db.String(50), nullable=False, default="C.C 1028140776")
    age = db.Column(db.String(20), nullable=False, default="19 años")
    title = db.Column(db.String(150), nullable=False, default="Estudiante de Ingeniería Informática | Full Stack Developer")
    university = db.Column(db.String(150), nullable=False, default="Universidad Tecnológica")
    career = db.Column(db.String(120), nullable=False, default="Ingeniería Informática")
    semester = db.Column(db.String(50), nullable=False, default="6.° Semestre")
    short_intro = db.Column(db.Text, nullable=False, default="Estudiante de 19 años de Ingeniería Informática enfocado en arquitectura de software, backend con Python/Flask e interfaces modernas.")
    bio = db.Column(db.Text, nullable=False, default="Soy Juan Miguel Duarte Castañeda, estudiante de 19 años de Ingeniería Informática radicado en La Estrella, Antioquia. Apasionado por la ingeniería de software, el diseño de sistemas y las aplicaciones full stack con bases sólidas en algoritmia y bases de datos relacionales.")
    objectives = db.Column(db.Text, nullable=False, default="Consolidar mi formación profesional como Ingeniero Informático aportando valor técnico en el desarrollo de plataformas seguras, escalables y con código mantenible.")
    interests_text = db.Column(db.Text, nullable=False, default="Desarrollo Web Full Stack, Arquitectura de Software, Inteligencia Artificial, Automatización de Procesos y Ciberseguridad.")
    email = db.Column(db.String(120), nullable=False, default="juan.duarte@universidad.edu.co")
    phone = db.Column(db.String(50), nullable=True, default="+57 312 456 7890")
    location = db.Column(db.String(100), nullable=False, default="La Estrella, Antioquia")
    github_url = db.Column(db.String(255), nullable=True, default="https://github.com/portlife")
    linkedin_url = db.Column(db.String(255), nullable=True, default="https://linkedin.com/in/portlife-estudiante")
    avatar_url = db.Column(db.String(255), nullable=False, default="/static/img/student_avatar.jpg")
    cv_url = db.Column(db.String(255), nullable=True, default="")
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "document_id": self.document_id,
            "age": self.age,
            "title": self.title,
            "university": self.university,
            "career": self.career,
            "semester": self.semester,
            "short_intro": self.short_intro,
            "bio": self.bio,
            "objectives": self.objectives,
            "interests_text": self.interests_text,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "github_url": self.github_url,
            "linkedin_url": self.linkedin_url,
            "avatar_url": self.avatar_url,
            "cv_url": self.cv_url,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Project(db.Model):
    """Proyectos realizados con estado, enlaces y tecnologías."""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(60), nullable=False, default="Full Stack")
    short_desc = db.Column(db.String(255), nullable=False)
    full_desc = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False, default="/static/img/glucokids.jpg")
    technologies = db.Column(db.String(255), nullable=False)  # Comma-separated list
    status = db.Column(db.String(50), nullable=False, default="En desarrollo") # Culminado, En desarrollo, Prototipo
    github_url = db.Column(db.String(255), nullable=True, default="")
    demo_url = db.Column(db.String(255), nullable=True, default="")
    featured = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    def get_tech_list(self):
        """Retorna lista limpia de tecnologías."""
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "category": self.category,
            "short_desc": self.short_desc,
            "full_desc": self.full_desc,
            "image_url": self.image_url,
            "technologies": self.get_tech_list(),
            "status": self.status,
            "github_url": self.github_url,
            "demo_url": self.demo_url,
            "featured": self.featured,
            "order": self.order
        }


class Study(db.Model):
    """Estudios y trayectoria académica del estudiante."""
    __tablename__ = 'studies'

    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    period = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="En curso") # En curso, Culminado
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "degree": self.degree,
            "institution": self.institution,
            "period": self.period,
            "status": self.status,
            "is_current": self.is_current,
            "description": self.description,
            "order": self.order
        }


class Skill(db.Model):
    """Lenguajes, frameworks y tecnologías con niveles reales."""
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(50), nullable=False, default="Backend") # Frontend, Backend, Base de Datos, Herramientas
    proficiency_level = db.Column(db.String(50), nullable=False, default="Intermedio") # Básico, Intermedio, Avanzado
    percentage = db.Column(db.Integer, nullable=False, default=75) # 0 to 100
    icon_class = db.Column(db.String(100), nullable=False, default="bi bi-code-slash")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "proficiency_level": self.proficiency_level,
            "percentage": self.percentage,
            "icon_class": self.icon_class,
            "order": self.order
        }


class InterestArea(db.Model):
    """Áreas de interés profesional de la carrera."""
    __tablename__ = 'interest_areas'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon_class = db.Column(db.String(100), nullable=False, default="bi bi-laptop")
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "icon_class": self.icon_class,
            "order": self.order
        }


class ContactMessage(db.Model):
    """Mensajes recibidos a través del formulario de contacto."""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
