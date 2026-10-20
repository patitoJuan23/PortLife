/**
 * PORTLIFE - SCRIPTS DE INTERACCIÓN PRINCIPALES
 * Manejo de navegación, filtros de proyectos, modal interactivo y envío AJAX de contacto.
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavbarScroll();
    initProjectFilters();
    initProjectModal();
    initContactForm();
    initSkillAnimation();
});

/**
 * Efecto de desenfoque y reducción de tamaño en el navbar al scrollear
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar-custom');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.style.padding = '0.5rem 0';
            navbar.style.background = 'rgba(7, 12, 27, 0.95)';
            navbar.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.5)';
        } else {
            navbar.style.padding = '0.8rem 0';
            navbar.style.background = 'rgba(7, 12, 27, 0.85)';
            navbar.style.boxShadow = 'none';
        }
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
            filterButtons.forEach(b => b.classList.remove('active', 'btn-electric'));
            filterButtons.forEach(b => b.classList.add('btn-glass'));
            
            btn.classList.remove('btn-glass');
            btn.classList.add('active', 'btn-electric');

            const filterValue = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                const category = card.getAttribute('data-category') || '';
                if (filterValue === 'all' || category.toLowerCase().includes(filterValue.toLowerCase())) {
                    card.style.display = 'block';
                    card.classList.add('animate__fadeIn');
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

/**
 * Modal dinámico con información detallada de cada proyecto
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
            
            // Cargar datos vía REST API
            fetch(`/api/projects/${projectId}`)
                .then(response => {
                    if (!response.ok) throw new Error('Error al cargar proyecto');
                    return response.json();
                })
                .then(data => {
                    modalTitle.textContent = data.title;
                    modalImage.src = data.image_url;
                    modalImage.alt = data.title;
                    modalCategory.textContent = data.category;
                    modalStatus.textContent = data.status;
                    modalDescription.textContent = data.full_desc || data.short_desc;

                    // Renderizar badges de tecnologías
                    modalTechBadges.innerHTML = '';
                    if (data.technologies && data.technologies.length > 0) {
                        data.technologies.forEach(tech => {
                            const badge = document.createElement('span');
                            badge.className = 'tech-badge';
                            badge.textContent = tech;
                            modalTechBadges.appendChild(badge);
                        });
                    }

                    // Enlaces
                    if (data.github_url && data.github_url.trim() !== '') {
                        modalGithubLink.href = data.github_url;
                        modalGithubLink.style.display = 'inline-flex';
                    } else {
                        modalGithubLink.style.display = 'none';
                    }

                    if (data.demo_url && data.demo_url.trim() !== '') {
                        modalDemoLink.href = data.demo_url;
                        modalDemoLink.style.display = 'inline-flex';
                    } else {
                        modalDemoLink.style.display = 'none';
                    }

                    modal.show();
                })
                .catch(err => {
                    console.error("Error al obtener detalles del proyecto:", err);
                    alert("No se pudo cargar la información detallada del proyecto.");
                });
        });
    });
}

/**
 * Manejo del formulario de contacto con validación y AJAX
 */
function initContactForm() {
    const contactForm = document.getElementById('contactForm');
    const feedbackBox = document.getElementById('contactFeedback');
    const submitBtn = document.getElementById('contactSubmitBtn');

    if (!contactForm) return;

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const nameInput = document.getElementById('contactName');
        const emailInput = document.getElementById('contactEmail');
        const subjectInput = document.getElementById('contactSubject');
        const messageInput = document.getElementById('contactMessage');

        // Validación cliente
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const subject = subjectInput.value.trim();
        const message = messageInput.value.trim();

        feedbackBox.innerHTML = '';
        feedbackBox.style.display = 'none';

        if (!name || name.length < 2) {
            showFeedback('Por favor ingresa tu nombre completo.', 'danger');
            nameInput.focus();
            return;
        }

        const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;
        if (!email || !emailRegex.test(email)) {
            showFeedback('Por favor proporciona una dirección de correo válida.', 'danger');
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

        // Estado cargando
        const originalBtnHtml = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Guardando en base de datos...';

        try {
            const response = await fetch('/contacto', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    subject: subject,
                    message: message
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                showFeedback(`✅ ${result.message}`, 'success');
                contactForm.reset();
            } else {
                const errList = result.errors ? result.errors.join('<br>') : (result.error || 'Ocurrió un error al guardar el mensaje.');
                showFeedback(`⚠️ ${errList}`, 'danger');
            }
        } catch (error) {
            console.error('Error enviando contacto:', error);
            showFeedback('❌ Error de conexión con el servidor. Por favor verifica tu conexión.', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnHtml;
        }
    });

    function showFeedback(msg, type) {
        feedbackBox.className = `alert alert-${type} mt-3 mb-0`;
        feedbackBox.innerHTML = msg;
        feedbackBox.style.display = 'block';
        feedbackBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * Animación fluida de barras de habilidades al entrar en el viewport
 */
function initSkillAnimation() {
    const skillBars = document.querySelectorAll('.skill-progress-fill');
    if (!skillBars.length) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const percent = bar.getAttribute('data-percent') || '0';
                bar.style.width = percent + '%';
                obs.unobserve(bar);
            }
        });
    }, { threshold: 0.3 });

    skillBars.forEach(bar => {
        bar.style.width = '0%';
        observer.observe(bar);
    });
}
