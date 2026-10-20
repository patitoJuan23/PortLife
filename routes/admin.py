from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Profile, Project, Study, Skill, InterestArea, ContactMessage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ==========================================
# AUTENTICACIÓN
# ==========================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión administrativo seguro."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not username or not password:
            flash("Por favor ingresa usuario y contraseña.", "warning")
            return render_template('admin/login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f"¡Bienvenido de nuevo, {user.username}!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash("Credenciales inválidas. Verifica tu usuario y contraseña.", "danger")

    return render_template('admin/login.html')


@admin_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Cierra la sesión administrativa."""
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('admin.login'))


# ==========================================
# DASHBOARD
# ==========================================

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Vista general y estadísticas del portafolio."""
    total_projects = Project.query.count()
    total_studies = Study.query.count()
    total_skills = Skill.query.count()
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()

    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    profile = Profile.query.first()

    return render_template(
        'admin/dashboard.html',
        total_projects=total_projects,
        total_studies=total_studies,
        total_skills=total_skills,
        total_messages=total_messages,
        unread_messages=unread_messages,
        recent_messages=recent_messages,
        recent_projects=recent_projects,
        profile=profile
    )


# ==========================================
# PERFIL
# ==========================================

@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_view():
    """Actualización de la información del perfil del estudiante."""
    profile = Profile.query.first()
    if not profile:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    if request.method == 'POST':
        profile.full_name = request.form.get('full_name', '').strip() or profile.full_name
        profile.title = request.form.get('title', '').strip() or profile.title
        profile.university = request.form.get('university', '').strip() or profile.university
        profile.career = request.form.get('career', '').strip() or profile.career
        profile.semester = request.form.get('semester', '').strip() or profile.semester
        profile.short_intro = request.form.get('short_intro', '').strip() or profile.short_intro
        profile.bio = request.form.get('bio', '').strip() or profile.bio
        profile.objectives = request.form.get('objectives', '').strip() or profile.objectives
        profile.interests_text = request.form.get('interests_text', '').strip() or profile.interests_text
        profile.email = request.form.get('email', '').strip() or profile.email
        profile.phone = request.form.get('phone', '').strip()
        profile.location = request.form.get('location', '').strip() or profile.location
        profile.github_url = request.form.get('github_url', '').strip()
        profile.linkedin_url = request.form.get('linkedin_url', '').strip()
        profile.avatar_url = request.form.get('avatar_url', '').strip() or profile.avatar_url

        try:
            db.session.commit()
            flash("Información del perfil actualizada exitosamente.", "success")
            return redirect(url_for('admin.profile_view'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar perfil: {str(e)}", "danger")

    return render_template('admin/profile.html', profile=profile)


# ==========================================
# PROYECTOS (CRUD)
# ==========================================

@admin_bp.route('/projects')
@login_required
def projects_list():
    """Listado y gestión de proyectos."""
    projects = Project.query.order_by(Project.order.asc(), Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)


@admin_bp.route('/projects/create', methods=['POST'])
@login_required
def project_create():
    """Crea un nuevo proyecto en el portafolio."""
    title = request.form.get('title', '').strip()
    category = request.form.get('category', '').strip() or "Full Stack"
    short_desc = request.form.get('short_desc', '').strip()
    full_desc = request.form.get('full_desc', '').strip()
    technologies = request.form.get('technologies', '').strip()
    status = request.form.get('status', '').strip() or "En desarrollo"
    image_url = request.form.get('image_url', '').strip() or "/static/img/glucokids.jpg"
    github_url = request.form.get('github_url', '').strip()
    demo_url = request.form.get('demo_url', '').strip()
    order = int(request.form.get('order', 0) or 0)
    featured = bool(request.form.get('featured'))

    if not title or not short_desc or not technologies:
        flash("Título, resumen y tecnologías son obligatorios.", "warning")
        return redirect(url_for('admin.projects_list'))

    # Generar slug simple y seguro
    base_slug = "".join(c.lower() if c.isalnum() else '-' for c in title).strip('-')
    slug = base_slug
    idx = 1
    while Project.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{idx}"
        idx += 1

    new_project = Project(
        title=title,
        slug=slug,
        category=category,
        short_desc=short_desc,
        full_desc=full_desc or short_desc,
        technologies=technologies,
        status=status,
        image_url=image_url,
        github_url=github_url,
        demo_url=demo_url,
        order=order,
        featured=featured
    )

    try:
        db.session.add(new_project)
        db.session.commit()
        flash(f"Proyecto '{title}' creado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar proyecto: {str(e)}", "danger")

    return redirect(url_for('admin.projects_list'))


@admin_bp.route('/projects/<int:project_id>/edit', methods=['POST'])
@login_required
def project_edit(project_id):
    """Actualiza los datos de un proyecto."""
    project = db.get_or_404(Project, project_id)

    project.title = request.form.get('title', '').strip() or project.title
    project.category = request.form.get('category', '').strip() or project.category
    project.short_desc = request.form.get('short_desc', '').strip() or project.short_desc
    project.full_desc = request.form.get('full_desc', '').strip() or project.full_desc
    project.technologies = request.form.get('technologies', '').strip() or project.technologies
    project.status = request.form.get('status', '').strip() or project.status
    project.image_url = request.form.get('image_url', '').strip() or project.image_url
    project.github_url = request.form.get('github_url', '').strip()
    project.demo_url = request.form.get('demo_url', '').strip()
    project.order = int(request.form.get('order', 0) or 0)
    project.featured = bool(request.form.get('featured'))

    try:
        db.session.commit()
        flash(f"Proyecto '{project.title}' actualizado exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar proyecto: {str(e)}", "danger")

    return redirect(url_for('admin.projects_list'))


@admin_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def project_delete(project_id):
    """Elimina un proyecto."""
    project = db.get_or_404(Project, project_id)
    title = project.title
    try:
        db.session.delete(project)
        db.session.commit()
        flash(f"Proyecto '{title}' eliminado correctamente.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar proyecto: {str(e)}", "danger")

    return redirect(url_for('admin.projects_list'))


# ==========================================
# ESTUDIOS (CRUD)
# ==========================================

@admin_bp.route('/studies')
@login_required
def studies_list():
    """Listado y gestión de estudios académicos."""
    studies = Study.query.order_by(Study.order.asc()).all()
    return render_template('admin/studies.html', studies=studies)


@admin_bp.route('/studies/create', methods=['POST'])
@login_required
def study_create():
    """Registra un nuevo estudio o formación."""
    degree = request.form.get('degree', '').strip()
    institution = request.form.get('institution', '').strip()
    period = request.form.get('period', '').strip()
    status = request.form.get('status', '').strip() or "En curso"
    is_current = bool(request.form.get('is_current'))
    description = request.form.get('description', '').strip()
    order = int(request.form.get('order', 0) or 0)

    if not degree or not institution or not period:
        flash("Título/Carrera, Institución y Periodo son obligatorios.", "warning")
        return redirect(url_for('admin.studies_list'))

    new_study = Study(
        degree=degree,
        institution=institution,
        period=period,
        status=status,
        is_current=is_current,
        description=description,
        order=order
    )

    try:
        db.session.add(new_study)
        db.session.commit()
        flash(f"Estudio '{degree}' añadido correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al registrar estudio: {str(e)}", "danger")

    return redirect(url_for('admin.studies_list'))


@admin_bp.route('/studies/<int:study_id>/edit', methods=['POST'])
@login_required
def study_edit(study_id):
    """Edita un estudio existente."""
    study = db.get_or_404(Study, study_id)
    study.degree = request.form.get('degree', '').strip() or study.degree
    study.institution = request.form.get('institution', '').strip() or study.institution
    study.period = request.form.get('period', '').strip() or study.period
    study.status = request.form.get('status', '').strip() or study.status
    study.is_current = bool(request.form.get('is_current'))
    study.description = request.form.get('description', '').strip()
    study.order = int(request.form.get('order', 0) or 0)

    try:
        db.session.commit()
        flash(f"Estudio '{study.degree}' modificado correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al editar estudio: {str(e)}", "danger")

    return redirect(url_for('admin.studies_list'))


@admin_bp.route('/studies/<int:study_id>/delete', methods=['POST'])
@login_required
def study_delete(study_id):
    """Elimina un estudio."""
    study = db.get_or_404(Study, study_id)
    degree = study.degree
    try:
        db.session.delete(study)
        db.session.commit()
        flash(f"Estudio '{degree}' eliminado con éxito.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")

    return redirect(url_for('admin.studies_list'))


# ==========================================
# HABILIDADES (CRUD)
# ==========================================

@admin_bp.route('/skills')
@login_required
def skills_list():
    """Listado y gestión de habilidades tecnológicas."""
    skills = Skill.query.order_by(Skill.category.asc(), Skill.order.asc()).all()
    return render_template('admin/skills.html', skills=skills)


@admin_bp.route('/skills/create', methods=['POST'])
@login_required
def skill_create():
    """Añade una nueva tecnología o habilidad."""
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip() or "Backend"
    proficiency_level = request.form.get('proficiency_level', '').strip() or "Intermedio"
    percentage = int(request.form.get('percentage', 70) or 70)
    icon_class = request.form.get('icon_class', '').strip() or "bi bi-code-slash"
    order = int(request.form.get('order', 0) or 0)

    if not name:
        flash("El nombre de la tecnología es obligatorio.", "warning")
        return redirect(url_for('admin.skills_list'))

    new_skill = Skill(
        name=name,
        category=category,
        proficiency_level=proficiency_level,
        percentage=min(max(percentage, 10), 100),
        icon_class=icon_class,
        order=order
    )

    try:
        db.session.add(new_skill)
        db.session.commit()
        flash(f"Tecnología '{name}' agregada con éxito.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear habilidad: {str(e)}", "danger")

    return redirect(url_for('admin.skills_list'))


@admin_bp.route('/skills/<int:skill_id>/edit', methods=['POST'])
@login_required
def skill_edit(skill_id):
    """Actualiza una tecnología."""
    skill = db.get_or_404(Skill, skill_id)
    skill.name = request.form.get('name', '').strip() or skill.name
    skill.category = request.form.get('category', '').strip() or skill.category
    skill.proficiency_level = request.form.get('proficiency_level', '').strip() or skill.proficiency_level
    skill.percentage = min(max(int(request.form.get('percentage', 70) or 70), 10), 100)
    skill.icon_class = request.form.get('icon_class', '').strip() or skill.icon_class
    skill.order = int(request.form.get('order', 0) or 0)

    try:
        db.session.commit()
        flash(f"Habilidad '{skill.name}' actualizada exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar: {str(e)}", "danger")

    return redirect(url_for('admin.skills_list'))


@admin_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def skill_delete(skill_id):
    """Elimina una habilidad."""
    skill = db.get_or_404(Skill, skill_id)
    name = skill.name
    try:
        db.session.delete(skill)
        db.session.commit()
        flash(f"Habilidad '{name}' eliminada correctamente.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {str(e)}", "danger")

    return redirect(url_for('admin.skills_list'))


# ==========================================
# MENSAJES DE CONTACTO
# ==========================================

@admin_bp.route('/messages')
@login_required
def messages_list():
    """Consulta y gestión de mensajes de contacto recibidos."""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)


@admin_bp.route('/messages/<int:message_id>/toggle-read', methods=['POST'])
@login_required
def message_toggle_read(message_id):
    """Alterna el estado leído/no leído de un mensaje."""
    msg = db.get_or_404(ContactMessage, message_id)
    msg.is_read = not msg.is_read
    db.session.commit()
    flash(f"Mensaje marcado como {'leído' if msg.is_read else 'no leído'}.", "success")
    return redirect(url_for('admin.messages_list'))


@admin_bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@login_required
def message_delete(message_id):
    """Elimina un mensaje de contacto."""
    msg = db.get_or_404(ContactMessage, message_id)
    try:
        db.session.delete(msg)
        db.session.commit()
        flash("Mensaje eliminado del sistema.", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar mensaje: {str(e)}", "danger")

    return redirect(url_for('admin.messages_list'))
