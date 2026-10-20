"""
Módulo de inicialización y carga de datos iniciales para PortLife.
Garantiza que la base de datos cuente con información realista y profesional sin inventar datos sensibles.
"""
from models import db, User, Profile, Project, Study, Skill, InterestArea

def seed_database(app):
    """Crea las tablas y puebla los datos iniciales si la BD está vacía."""
    with app.app_context():
        db.create_all()

        # 1. Crear usuario administrador por defecto si no existe
        admin = User.query.first()
        if not admin:
            admin_user = app.config.get('ADMIN_USERNAME', 'admin')
            admin_email = app.config.get('ADMIN_EMAIL', 'admin@portlife.dev')
            admin_pass = app.config.get('ADMIN_PASSWORD', 'admin123')

            admin = User(
                username=admin_user,
                email=admin_email
            )
            admin.set_password(admin_pass)
            db.session.add(admin)
            print(f"[Seed] Usuario administrador creado: {admin_user}")

        # 2. Perfil del estudiante
        if not Profile.query.first():
            profile = Profile(
                full_name="Alex Rendón",
                title="Estudiante de Ingeniería Informática | Desarrollador Full Stack",
                university="Universidad Tecnológica",
                career="Ingeniería Informática",
                semester="6.° Semestre",
                short_intro="Estudiante universitario enfocado en desarrollo web moderno, arquitectura de software y creación de soluciones prácticas con Python, Flask y tecnologías web.",
                bio="Soy estudiante de 6.° semestre de Ingeniería Informática con gran vocación por la ingeniería de software y el desarrollo full stack. Cuento con bases sólidas en algoritmia, bases de datos relacionales, programación estructurada y orientada a objetos. Me apasiona transformar requerimientos en plataformas estables, bien documentadas y con una excelente experiencia de usuario.",
                objectives="Consolidar mi formación como Ingeniero Informático participando en proyectos desafiantes donde pueda aplicar patrones de diseño, desarrollo backend con Python/Flask, gestión de bases de datos y buenas prácticas de seguridad e interfaces de usuario.",
                interests_text="Desarrollo Web Full Stack, Arquitectura de Software, Inteligencia Artificial, Automatización de Procesos y Ciberseguridad.",
                email="alex.rendon@universidad.edu.co",
                phone="+57 312 456 7890",
                location="Medellín, Colombia",
                github_url="https://github.com/portlife",
                linkedin_url="https://linkedin.com/in/portlife-estudiante",
                avatar_url="/static/img/student_avatar.jpg",
                cv_url=""
            )
            db.session.add(profile)
            print("[Seed] Perfil inicial creado.")

        # 3. Proyectos requeridos
        if not Project.query.first():
            projects = [
                Project(
                    title="GlucoKids",
                    slug="glucokids",
                    category="Salud Digital / Web",
                    short_desc="Plataforma interactiva para el monitoreo glucémico y educación lúdica en niños con diabetes tipo 1.",
                    full_desc="GlucoKids es una solución tecnológica diseñada para empoderar a niños y familias en el control diario de la diabetes. Incorpora registro visual de glucosa, alertas automáticas, seguimiento de dosis y un módulo lúdico que premia la constancia del paciente con insignias de logro.",
                    image_url="/static/img/glucokids.jpg",
                    technologies="Python, Flask, SQLite, Bootstrap 5, JavaScript, Chart.js",
                    status="En desarrollo",
                    github_url="https://github.com/portlife/glucokids",
                    demo_url="#demo-glucokids",
                    featured=True,
                    order=1
                ),
                Project(
                    title="PetCare",
                    slug="petcare",
                    category="Gestión / Full Stack",
                    short_desc="Sistema de administración clínica veterinaria para historial médico digital y agendamiento de pacientes.",
                    full_desc="PetCare optimiza la gestión operativa y asistencial de clínicas veterinarias. Facilita el registro de pacientes caninos y felinos, historial de vacunación, evolución de tratamientos, prescripciones médicas y recordatorios automáticos para los tutores.",
                    image_url="/static/img/petcare.jpg",
                    technologies="Python, Flask, SQLAlchemy, JavaScript, Bootstrap 5, HTML5, CSS3",
                    status="Culminado",
                    github_url="https://github.com/portlife/petcare",
                    demo_url="#demo-petcare",
                    featured=True,
                    order=2
                ),
                Project(
                    title="Hablemos",
                    slug="hablemos",
                    category="Bienestar Social / Web",
                    short_desc="Plataforma de soporte y comunicación comunitaria enfocada en bienestar emocional y orientación.",
                    full_desc="Hablemos es un espacio web seguro y anónimo que fomenta el bienestar emocional en comunidades universitarias. Ofrece un diario interactivo del estado de ánimo, foros temáticos moderados y enlace directo con orientadores estudiantiles.",
                    image_url="/static/img/hablemos.jpg",
                    technologies="Python, Flask, SQLite, JavaScript, Bootstrap 5, CSS3",
                    status="Prototipo funcional",
                    github_url="https://github.com/portlife/hablemos",
                    demo_url="#demo-hablemos",
                    featured=True,
                    order=3
                )
            ]
            db.session.add_all(projects)
            print("[Seed] Proyectos iniciales creados.")

        # 4. Formación académica
        if not Study.query.first():
            studies = [
                Study(
                    degree="Ingeniería Informática",
                    institution="Universidad Tecnológica",
                    period="2022 - Actualidad",
                    status="En curso",
                    is_current=True,
                    description="Cursando 6.° semestre. Énfasis en algoritmia y estructuras de datos, diseño de bases de datos relacionales, arquitectura de software, redes de computadores y desarrollo web.",
                    order=1
                ),
                Study(
                    degree="Tecnología en Análisis y Desarrollo de Software",
                    institution="Instituto de Educación Técnica",
                    period="2020 - 2022",
                    status="Culminado",
                    is_current=False,
                    description="Fundamentos de programación estructurada y orientada a objetos, modelado conceptual y lógico de bases de datos y desarrollo de proyectos prácticos.",
                    order=2
                ),
                Study(
                    degree="Diplomado en Desarrollo Backend con Python & Flask",
                    institution="Centro de Innovación Tecnológica",
                    period="2023",
                    status="Culminado",
                    is_current=False,
                    description="Profundización en desarrollo web con Flask, autenticación segura, creación de APIs RESTful, manejo de SQLAlchemy y despliegue de aplicaciones en servidores Linux.",
                    order=3
                )
            ]
            db.session.add_all(studies)
            print("[Seed] Formación académica creada.")

        # 5. Habilidades y tecnologías con niveles realistas
        if not Skill.query.first():
            skills = [
                # Frontend
                Skill(name="HTML5", category="Frontend", proficiency_level="Avanzado", percentage=90, icon_class="bi bi-filetype-html", order=1),
                Skill(name="CSS3", category="Frontend", proficiency_level="Intermedio-Avanzado", percentage=85, icon_class="bi bi-filetype-css", order=2),
                Skill(name="JavaScript", category="Frontend", proficiency_level="Intermedio", percentage=80, icon_class="bi bi-filetype-js", order=3),
                Skill(name="Bootstrap 5", category="Frontend", proficiency_level="Avanzado", percentage=88, icon_class="bi bi-bootstrap-fill", order=4),
                # Backend
                Skill(name="Python", category="Backend", proficiency_level="Intermedio-Avanzado", percentage=85, icon_class="bi bi-filetype-py", order=5),
                Skill(name="Flask", category="Backend", proficiency_level="Intermedio", percentage=82, icon_class="bi bi-fire", order=6),
                Skill(name="API REST", category="Backend", proficiency_level="Intermedio", percentage=80, icon_class="bi bi-arrow-left-right", order=7),
                # Bases de Datos
                Skill(name="SQL & Modelado Relacional", category="Bases de Datos", proficiency_level="Intermedio", percentage=82, icon_class="bi bi-database", order=8),
                Skill(name="SQLite & PostgreSQL", category="Bases de Datos", proficiency_level="Intermedio", percentage=78, icon_class="bi bi-server", order=9),
                # Herramientas
                Skill(name="Git & GitHub", category="Herramientas", proficiency_level="Intermedio-Avanzado", percentage=85, icon_class="bi bi-git", order=10),
                Skill(name="Linux / Bash", category="Herramientas", proficiency_level="Intermedio", percentage=75, icon_class="bi bi-terminal-fill", order=11)
            ]
            db.session.add_all(skills)
            print("[Seed] Habilidades tecnológicas creadas.")

        # 6. Áreas de interés profesional
        if not InterestArea.query.first():
            areas = [
                InterestArea(
                    title="Desarrollo Web Full Stack",
                    description="Diseño y construcción de aplicaciones integrales conectando interfaces modernas, accesibles y responsivas con servicios backend estructurados y seguros.",
                    icon_class="bi bi-code-slash",
                    order=1
                ),
                InterestArea(
                    title="Inteligencia Artificial y Datos",
                    description="Investigación y aplicación de técnicas de aprendizaje automático, procesamiento de datos y algoritmos inteligentes para resolver problemas complejos del entorno.",
                    icon_class="bi bi-cpu-fill",
                    order=2
                ),
                InterestArea(
                    title="Automatización de Procesos",
                    description="Creación de scripts, tareas programadas e integración de herramientas que aumenten la eficiencia y reduzcan el error humano en operaciones repetitivas.",
                    icon_class="bi bi-gear-wide-connected",
                    order=3
                ),
                InterestArea(
                    title="Creación de Aplicaciones de Impacto",
                    description="Ingeniería orientada a software de utilidad comunitaria y empresarial, con estándares de arquitectura limpia y enfoque centrado en las personas.",
                    icon_class="bi bi-grid-1x2-fill",
                    order=4
                )
            ]
            db.session.add_all(areas)
            print("[Seed] Áreas de interés creadas.")

        db.session.commit()
        print("[Seed] Base de datos inicializada y confirmada exitosamente.")
