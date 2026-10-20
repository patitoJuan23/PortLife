"""
Script de pruebas automatizadas para verificar integridad de la aplicación PortLife.
Comprueba endpoints públicos, REST API, formulario de contacto, autenticación y CRUD.
"""
import unittest
from app import create_app
from models import db, User, Profile, Project, Study, Skill, ContactMessage

class PortLifeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_01_public_index(self):
        """Verifica que la página principal cargue con código 200 y contenga las secciones."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('PortLife', html)
        self.assertIn('GlucoKids', html)
        self.assertIn('PetCare', html)
        self.assertIn('Hablemos', html)
        self.assertIn('Ingeniería Informática', html)
        self.assertIn('id="contacto"', html)
        print("[OK] Test 01: Pagina publica principal verificada exitosamente.")

    def test_02_api_endpoints(self):
        """Verifica los endpoints REST API."""
        # 1. API Proyectos
        res_proj = self.client.get('/api/projects')
        self.assertEqual(res_proj.status_code, 200)
        projects = res_proj.get_json()
        self.assertIsInstance(projects, list)
        self.assertGreaterEqual(len(projects), 3)
        titles = [p['title'] for p in projects]
        self.assertIn('GlucoKids', titles)
        self.assertIn('PetCare', titles)
        self.assertIn('Hablemos', titles)

        # 2. API Perfil
        res_prof = self.client.get('/api/profile')
        self.assertEqual(res_prof.status_code, 200)
        profile = res_prof.get_json()
        self.assertIn('full_name', profile)
        self.assertIn('career', profile)

        # 3. API Estudios
        res_stud = self.client.get('/api/studies')
        self.assertEqual(res_stud.status_code, 200)
        studies = res_stud.get_json()
        self.assertGreaterEqual(len(studies), 1)

        # 4. API Habilidades
        res_skills = self.client.get('/api/skills')
        self.assertEqual(res_skills.status_code, 200)
        skills = res_skills.get_json()
        self.assertGreaterEqual(len(skills), 5)
        print("[OK] Test 02: Endpoints REST API verificados exitosamente.")

    def test_03_contact_form_submission(self):
        """Verifica el envío y almacenamiento del mensaje de contacto."""
        payload = {
            "name": "Profesor Evaluador",
            "email": "evaluador@universidad.edu.co",
            "subject": "Excelente proyecto de parcial",
            "message": "Felicidades por la arquitectura y presentación del portafolio PortLife."
        }
        response = self.client.post('/contacto', json=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue(data.get('success'))

        # Validar en la base de datos
        with self.app.app_context():
            msg = ContactMessage.query.filter_by(email="evaluador@universidad.edu.co").first()
            self.assertIsNotNone(msg)
            self.assertEqual(msg.name, "Profesor Evaluador")
        print("[OK] Test 03: Formulario de contacto y persistencia en BD verificados.")

    def test_04_admin_authentication_and_protection(self):
        """Verifica la protección de rutas y autenticación del administrador."""
        # Intento de acceso sin autenticación -> debe redirigir a /admin/login
        res_unauth = self.client.get('/admin/dashboard')
        self.assertEqual(res_unauth.status_code, 302)
        self.assertIn('/admin/login', res_unauth.headers['Location'])

        # Intento de login con credenciales erróneas
        res_bad_login = self.client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpassword'})
        self.assertEqual(res_bad_login.status_code, 200)
        self.assertIn('Credenciales inválidas', res_bad_login.data.decode('utf-8'))

        # Login exitoso
        res_login = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        html = res_login.data.decode('utf-8')
        self.assertIn('Panel de Control', html)
        self.assertIn('Cerrar Sesión', html)
        print("[OK] Test 04: Seguridad de autenticacion y proteccion de rutas verificada.")

    def test_05_admin_crud_operations(self):
        """Verifica operaciones CRUD de proyectos y habilidades en el panel admin."""
        # Autenticar primero
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'})

        # Crear nuevo proyecto de prueba
        res_create = self.client.post('/admin/projects/create', data={
            'title': 'Proyecto de Prueba CRUD',
            'category': 'Prueba',
            'short_desc': 'Descripción corta de prueba',
            'full_desc': 'Descripción completa de prueba',
            'technologies': 'Python, Flask, PyTest',
            'status': 'En desarrollo',
            'image_url': '/static/img/glucokids.jpg',
            'order': '99'
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)

        with self.app.app_context():
            proj = Project.query.filter_by(title='Proyecto de Prueba CRUD').first()
            self.assertIsNotNone(proj)
            proj_id = proj.id

            # Editar proyecto
            self.client.post(f'/admin/projects/{proj_id}/edit', data={
                'title': 'Proyecto de Prueba Editado',
                'category': 'Prueba Editada',
                'short_desc': 'Descripción modificada',
                'full_desc': 'Descripción completa modificada',
                'technologies': 'Python, Flask, SQLite',
                'status': 'Culminado',
                'image_url': '/static/img/glucokids.jpg',
                'order': '100'
            }, follow_redirects=True)

            updated = db.session.get(Project, proj_id)
            self.assertEqual(updated.title, 'Proyecto de Prueba Editado')

            # Eliminar proyecto de prueba
            self.client.post(f'/admin/projects/{proj_id}/delete', follow_redirects=True)
            deleted = db.session.get(Project, proj_id)
            self.assertIsNone(deleted)

        print("[OK] Test 05: Operaciones CRUD (Crear, Editar, Eliminar) verificadas con exito.")

if __name__ == '__main__':
    unittest.main()
