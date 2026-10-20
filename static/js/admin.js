/**
 * PORTLIFE - SCRIPTS DEL PANEL ADMINISTRATIVO
 * Funciones de edición modal, confirmaciones y gestión de datos.
 */

document.addEventListener('DOMContentLoaded', () => {
    initProjectEditModals();
    initStudyEditModals();
    initSkillEditModals();
});

/**
 * Carga de datos de proyecto en modal de edición
 */
function initProjectEditModals() {
    const editButtons = document.querySelectorAll('.btn-edit-project');
    const modalEl = document.getElementById('editProjectModal');
    if (!editButtons.length || !modalEl) return;

    const form = document.getElementById('editProjectForm');
    const titleInp = document.getElementById('editProjectTitle');
    const categoryInp = document.getElementById('editProjectCategory');
    const statusInp = document.getElementById('editProjectStatus');
    const orderInp = document.getElementById('editProjectOrder');
    const shortDescInp = document.getElementById('editProjectShortDesc');
    const fullDescInp = document.getElementById('editProjectFullDesc');
    const techsInp = document.getElementById('editProjectTechs');
    const imageInp = document.getElementById('editProjectImage');
    const githubInp = document.getElementById('editProjectGithub');
    const demoInp = document.getElementById('editProjectDemo');
    const featuredInp = document.getElementById('editProjectFeatured');

    editButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            form.action = `/admin/projects/${id}/edit`;

            titleInp.value = btn.getAttribute('data-title') || '';
            categoryInp.value = btn.getAttribute('data-category') || '';
            statusInp.value = btn.getAttribute('data-status') || 'En desarrollo';
            orderInp.value = btn.getAttribute('data-order') || '0';
            shortDescInp.value = btn.getAttribute('data-short-desc') || '';
            fullDescInp.value = btn.getAttribute('data-full-desc') || '';
            techsInp.value = btn.getAttribute('data-technologies') || '';
            imageInp.value = btn.getAttribute('data-image') || '';
            githubInp.value = btn.getAttribute('data-github') || '';
            demoInp.value = btn.getAttribute('data-demo') || '';
            featuredInp.checked = btn.getAttribute('data-featured') === 'True' || btn.getAttribute('data-featured') === 'true';
        });
    });
}

/**
 * Carga de datos de estudio en modal de edición
 */
function initStudyEditModals() {
    const editButtons = document.querySelectorAll('.btn-edit-study');
    const modalEl = document.getElementById('editStudyModal');
    if (!editButtons.length || !modalEl) return;

    const form = document.getElementById('editStudyForm');
    const degreeInp = document.getElementById('editStudyDegree');
    const instInp = document.getElementById('editStudyInstitution');
    const periodInp = document.getElementById('editStudyPeriod');
    const statusInp = document.getElementById('editStudyStatus');
    const orderInp = document.getElementById('editStudyOrder');
    const isCurrentInp = document.getElementById('editStudyCurrent');
    const descInp = document.getElementById('editStudyDescription');

    editButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            form.action = `/admin/studies/${id}/edit`;

            degreeInp.value = btn.getAttribute('data-degree') || '';
            instInp.value = btn.getAttribute('data-institution') || '';
            periodInp.value = btn.getAttribute('data-period') || '';
            statusInp.value = btn.getAttribute('data-status') || 'En curso';
            orderInp.value = btn.getAttribute('data-order') || '0';
            isCurrentInp.checked = btn.getAttribute('data-current') === 'True' || btn.getAttribute('data-current') === 'true';
            descInp.value = btn.getAttribute('data-description') || '';
        });
    });
}

/**
 * Carga de datos de habilidad en modal de edición
 */
function initSkillEditModals() {
    const editButtons = document.querySelectorAll('.btn-edit-skill');
    const modalEl = document.getElementById('editSkillModal');
    if (!editButtons.length || !modalEl) return;

    const form = document.getElementById('editSkillForm');
    const nameInp = document.getElementById('editSkillName');
    const catInp = document.getElementById('editSkillCategory');
    const levelInp = document.getElementById('editSkillLevel');
    const percentInp = document.getElementById('editSkillPercentage');
    const iconInp = document.getElementById('editSkillIcon');
    const orderInp = document.getElementById('editSkillOrder');

    editButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            form.action = `/admin/skills/${id}/edit`;

            nameInp.value = btn.getAttribute('data-name') || '';
            catInp.value = btn.getAttribute('data-category') || 'Backend';
            levelInp.value = btn.getAttribute('data-level') || 'Intermedio';
            percentInp.value = btn.getAttribute('data-percentage') || '75';
            iconInp.value = btn.getAttribute('data-icon') || 'bi bi-code-slash';
            orderInp.value = btn.getAttribute('data-order') || '0';
        });
    });
}
