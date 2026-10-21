/**
 * PORTLIFE - SCRIPTS DE INTERACCIÓN PRINCIPALES (VERSIÓN ESTÁTICA)
 * Compatible con ejecución directa (doble clic en index.html) y GitHub Pages.
 * No requiere Flask, Python ni servidor local.
 */

// Datos completos y detallados de los proyectos para apertura inmediata sin peticiones de red
const PROJECTS_DATA = {
    1: {
        id: 1,
        title: "GlucoKids",
        slug: "glucokids",
        category: "Salud Digital / Web",
        status: "En desarrollo",
        short_desc: "Plataforma interactiva para el monitoreo glucémico y educación lúdica en niños con diabetes tipo 1.",
        full_desc: "GlucoKids es una solución tecnológica diseñada para empoderar a niños y familias en el control diario de la diabetes. Incorpora registro visual de glucosa, alertas automáticas, seguimiento de dosis y un módulo lúdico que premia la constancia del paciente con insignias de logro.",
        image_url: "assets/glucokids.jpg",
        technologies: ["Python", "Flask", "SQLite", "Bootstrap 5", "JavaScript", "Chart.js"],
        github_url: "https://github.com/portlife/glucokids",
        demo_url: "#demo-glucokids"
    },
    2: {
        id: 2,
        title: "PetCare",
        slug: "petcare",
        category: "Gestión / Full Stack",
        status: "Culminado",
        short_desc: "Sistema de administración clínica veterinaria para historial médico digital y agendamiento de pacientes.",
        full_desc: "PetCare optimiza la gestión operativa y asistencial de clínicas veterinarias. Facilita el registro de pacientes caninos y felinos, historial de vacunación, evolución de tratamientos, prescripciones médicas y recordatorios automáticos para los tutores.",
        image_url: "assets/petcare.jpg",
        technologies: ["Python", "Flask", "SQLAlchemy", "JavaScript", "Bootstrap 5", "HTML5", "CSS3"],
        github_url: "https://github.com/portlife/petcare",
        demo_url: "#demo-petcare"
    },
    3: {
        id: 3,
        title: "Hablemos",
        slug: "hablemos",
        category: "Bienestar Social / Web",
        status: "Prototipo funcional",
        short_desc: "Plataforma de soporte y comunicación comunitaria enfocada en bienestar emocional y orientación.",
        full_desc: "Hablemos es un espacio web seguro y anónimo que fomenta el bienestar emocional en comunidades universitarias. Ofrece un diario interactivo del estado de ánimo, foros temáticos moderados y enlace directo con orientadores estudiantiles.",
        image_url: "assets/hablemos.jpg",
        technologies: ["Python", "Flask", "SQLite", "JavaScript", "Bootstrap 5", "CSS3"],
        github_url: "https://github.com/portlife/hablemos",
        demo_url: "#demo-hablemos"
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initNavbarScroll();
    initMobileNavClose();
    initProjectFilters();
    initProjectModal();
    initContactForm();
    initSkillAnimation();
});

/**
 * Efecto dinámico en el navbar al hacer scroll
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar-custom');
    if (!navbar) return;

    const handleScroll = () => {
        if (window.scrollY > 40) {
            navbar.style.padding = '0.5rem 0';
            navbar.style.background = 'rgba(7, 12, 27, 0.95)';
            navbar.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.5)';
        } else {
            navbar.style.padding = '0.8rem 0';
            navbar.style.background = 'rgba(7, 12, 27, 0.85)';
            navbar.style.boxShadow = 'none';
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
}

/**
 * Cierre automático del menú colapsable en dispositivos móviles al pulsar un enlace
 */
function initMobileNavClose() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link, .btn-nav-action');
    const navCollapse = document.getElementById('navbarContent');

    if (!navCollapse) return;

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navCollapse.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
        });
    });
}

/**
 * Filtro interactivo de proyectos por categoría
 */
function initProjectFilters() {
    const filterButtons = document.querySelectorAll('.project-filter-btn');
    const projectCards = document.querySelectorAll('.project-grid-item');

    if (!filterButtons.length || !projectCards.length) return;

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => {
                b.classList.remove('active', 'btn-electric');
                b.classList.add('btn-glass');
            });

            btn.classList.remove('btn-glass');
            btn.classList.add('active', 'btn-electric');

            const filterValue = btn.getAttribute('data-filter') || 'all';

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category') || '';
                if (filterValue === 'all' || category.toLowerCase().includes(filterValue.toLowerCase())) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Modal con información detallada de cada proyecto (100% autónomo y offline)
 */
function initProjectModal() {
    const detailButtons = document.querySelectorAll('.btn-project-detail');
    const modalElement = document.getElementById('projectDetailModal');
    if (!modalElement) return;

    const modal = new bootstrap.Modal(modalElement);
    const modalTitle = document.getElementById('modalProjectTitle');
    const modalImage = document.getElementById('modalProjectImage');
    const modalCategory = document.getElementById('modalProjectCategory');
    const modalStatus = document.getElementById('modalProjectStatus');
    const modalDescription = document.getElementById('modalProjectDesc');
    const modalTechBadges = document.getElementById('modalProjectTechs');
    const modalGithubLink = document.getElementById('modalProjectGithub');
    const modalDemoLink = document.getElementById('modalProjectDemo');

    detailButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const projectId = btn.getAttribute('data-id');
            const data = PROJECTS_DATA[projectId];

            if (!data) return;

            modalTitle.textContent = data.title;
            modalImage.src = data.image_url;
            modalImage.alt = "Vista previa de " + data.title;
            modalCategory.textContent = data.category;
            modalStatus.textContent = data.status;
            modalDescription.textContent = data.full_desc || data.short_desc;

            // Badges de tecnologías
            modalTechBadges.innerHTML = '';
            if (data.technologies && data.technologies.length > 0) {
                data.technologies.forEach(tech => {
                    const badge = document.createElement('span');
                    badge.className = 'tech-badge';
                    badge.textContent = tech;
                    modalTechBadges.appendChild(badge);
                });
            }

            // Enlace a GitHub
            if (data.github_url && data.github_url.trim() !== '') {
                modalGithubLink.href = data.github_url;
                modalGithubLink.style.display = 'inline-flex';
            } else {
                modalGithubLink.style.display = 'none';
            }

            // Enlace a Demostración
            if (data.demo_url && data.demo_url.trim() !== '') {
                modalDemoLink.href = data.demo_url;
                modalDemoLink.style.display = 'inline-flex';
            } else {
                modalDemoLink.style.display = 'none';
            }

            modal.show();
        });
    });
}

/**
 * Manejo del formulario de contacto con validación en tiempo real en frontend
 */
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    const feedbackBox = document.getElementById('contactFeedback');
    const submitBtn = document.getElementById('contactSubmitBtn');

    if (!contactForm) return;

    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const nameInput = document.getElementById('contactName');
        const emailInput = document.getElementById('contactEmail');
        const subjectInput = document.getElementById('contactSubject');
        const messageInput = document.getElementById('contactMessage');

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const subject = subjectInput.value.trim();
        const message = messageInput.value.trim();

        feedbackBox.innerHTML = '';
        feedbackBox.style.display = 'none';

        if (!name || name.length < 2) {
            showFeedback('Por favor ingresa tu nombre completo (mínimo 2 caracteres).', 'danger');
            nameInput.focus();
            return;
        }

        const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;
        if (!email || !emailRegex.test(email)) {
            showFeedback('Por favor proporciona una dirección de correo electrónico válida.', 'danger');
            emailInput.focus();
            return;
        }

        if (!subject || subject.length < 3) {
            showFeedback('El asunto debe tener al menos 3 caracteres.', 'danger');
            subjectInput.focus();
            return;
        }

        if (!message || message.length < 10) {
            showFeedback('El mensaje debe contener al menos 10 caracteres explicativos.', 'danger');
            messageInput.focus();
            return;
        }

        // Simulación de procesamiento y confirmación amigable
        const originalBtnHtml = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Procesando...';

        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHtml;

            // Mensaje de éxito con opción de envío directo por correo
            const mailtoUrl = `mailto:juan.duarte@universidad.edu.co?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent("Hola Juan Miguel,\n\n" + message + "\n\nDe: " + name + " (" + email + ")")}`;

            showFeedback(`
                <div class="d-flex flex-column gap-2">
                    <div>
                        <i class="bi bi-check-circle-fill text-success me-2 fs-5 align-middle"></i>
                        <strong>¡Mensaje validado con éxito, ${escapeHtml(name)}!</strong>
                    </div>
                    <p class="mb-2 small">Tu mensaje ha sido registrado correctamente en la interfaz del portafolio.</p>
                    <div>
                        <a href="${mailtoUrl}" class="btn btn-sm btn-electric mt-1">
                            <i class="bi bi-envelope-arrow-up-fill me-1"></i> Abrir en tu cliente de correo (Opcional)
                        </a>
                    </div>
                </div>
            `, 'success');

            contactForm.reset();
        }, 400);
    });

    function showFeedback(msg, type) {
        feedbackBox.className = `alert alert-${type} mt-3 mb-0`;
        feedbackBox.innerHTML = msg;
        feedbackBox.style.display = 'block';
        feedbackBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

/**
 * Animación suave de las barras de progreso de tecnologías al entrar en el viewport
 */
function initSkillAnimation() {
    const skillBars = document.querySelectorAll('.skill-progress-fill');
    if (!skillBars.length) return;

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const percent = bar.getAttribute('data-percent') || '0';
                    bar.style.width = percent + '%';
                    obs.unobserve(bar);
                }
            });
        }, { threshold: 0.2 });

        skillBars.forEach(bar => {
            bar.style.width = '0%';
            observer.observe(bar);
        });
    } else {
        // Fallback para navegadores antiguos
        skillBars.forEach(bar => {
            bar.style.width = (bar.getAttribute('data-percent') || '0') + '%';
        });
    }
}
