import re
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from models import db, Profile, Project, Study, Skill, InterestArea, ContactMessage

public_bp = Blueprint('public', __name__)

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

@public_bp.route('/')
def index():
    """Ruta principal del portafolio público."""
    profile = Profile.query.first()
    projects = Project.query.order_by(Project.order.asc(), Project.created_at.desc()).all()
    studies = Study.query.order_by(Study.order.asc()).all()
    skills = Skill.query.order_by(Skill.order.asc()).all()
    interests = InterestArea.query.order_by(InterestArea.order.asc()).all()

    # Agrupar habilidades por categoría para mostrarlas organizadas
    skills_by_category = {}
    for sk in skills:
        skills_by_category.setdefault(sk.category, []).append(sk)

    return render_template(
        'index.html',
        profile=profile,
        projects=projects,
        studies=studies,
        skills=skills,
        skills_by_category=skills_by_category,
        interests=interests
    )


@public_bp.route('/contacto', methods=['POST'])
def submit_contact():
    """Recibe y valida los mensajes enviados a través del formulario de contacto."""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

    if request.is_json:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
    else:
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

    # Validaciones en Backend
    errors = []
    if not name or len(name) < 2:
        errors.append("El nombre es requerido y debe tener al menos 2 caracteres.")
    if not email or not re.match(EMAIL_REGEX, email):
        errors.append("Por favor ingresa un correo electrónico válido.")
    if not subject or len(subject) < 3:
        errors.append("El asunto es requerido (mínimo 3 caracteres).")
    if not message or len(message) < 10:
        errors.append("El mensaje debe contener al menos 10 caracteres.")

    if errors:
        if is_ajax:
            return jsonify({"success": False, "errors": errors}), 400
        for err in errors:
            flash(err, "danger")
        return redirect(url_for('public.index') + "#contacto")

    try:
        new_msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_msg)
        db.session.commit()

        success_text = "¡Gracias por contactarme! Tu mensaje ha sido guardado exitosamente en la base de datos."
        if is_ajax:
            return jsonify({
                "success": True,
                "message": success_text,
                "id": new_msg.id
            }), 201
        
        flash(success_text, "success")
        return redirect(url_for('public.index') + "#contacto")
    except Exception as e:
        db.session.rollback()
        error_msg = "Ocurrió un error al procesar el mensaje. Por favor intenta de nuevo más tarde."
        if is_ajax:
            return jsonify({"success": False, "errors": [error_msg]}), 500
        flash(error_msg, "danger")
        return redirect(url_for('public.index') + "#contacto")


# ==========================================
# ENDPOINTS REST API
# ==========================================

@public_bp.route('/api/profile', methods=['GET'])
def api_profile():
    """Consulta pública del perfil del estudiante en formato JSON."""
    profile = Profile.query.first()
    if not profile:
        return jsonify({"error": "Perfil no encontrado"}), 404
    return jsonify(profile.to_dict()), 200


@public_bp.route('/api/projects', methods=['GET'])
def api_projects():
    """Listado público de proyectos con filtros opcionales."""
    category = request.args.get('category')
    query = Project.query
    if category:
        query = query.filter_by(category=category)
    projects = query.order_by(Project.order.asc(), Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects]), 200


@public_bp.route('/api/projects/<int:project_id>', methods=['GET'])
def api_project_detail(project_id):
    """Consulta de detalle de un proyecto por ID."""
    project = db.get_or_404(Project, project_id)
    return jsonify(project.to_dict()), 200


@public_bp.route('/api/studies', methods=['GET'])
def api_studies():
    """Listado público de estudios y formación académica."""
    studies = Study.query.order_by(Study.order.asc()).all()
    return jsonify([s.to_dict() for s in studies]), 200


@public_bp.route('/api/skills', methods=['GET'])
def api_skills():
    """Listado público de habilidades y niveles técnicos."""
    skills = Skill.query.order_by(Skill.order.asc()).all()
    return jsonify([sk.to_dict() for sk in skills]), 200


@public_bp.route('/api/contact', methods=['POST'])
def api_contact():
    """Endpoint REST para recibir mensajes de contacto."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Cuerpo de solicitud JSON requerido"}), 400

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    errors = []
    if not name or len(name) < 2:
        errors.append("El nombre es requerido y debe tener al menos 2 caracteres.")
    if not email or not re.match(EMAIL_REGEX, email):
        errors.append("Correo electrónico inválido.")
    if not subject:
        errors.append("El asunto es requerido.")
    if not message or len(message) < 10:
        errors.append("El mensaje debe contener al menos 10 caracteres.")

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    try:
        new_msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_msg)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Mensaje recibido y almacenado exitosamente.",
            "data": new_msg.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": "Error interno al guardar el mensaje"}), 500
