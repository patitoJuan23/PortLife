"""
Suite de pruebas automatizadas actualizada para PortLife.
Verifica:
- Portal de inicio de sesión y registro (GET /)
- Portafolio público de Juan Miguel Duarte Castañeda (GET /portafolio)
- Registro de nuevo usuario (POST /register)
- Autenticación de usuario y administrador (POST /login)
- Endpoints REST API (/api/profile, /api/projects, etc.)
- Formulario de contacto y persistencia
- Operaciones CRUD en el panel administrativo
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

    def test_01_portal_auth_root(self):
        """Verifica que la raíz '/' sea el portal de inicio con Registro e Inicio de Sesión."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('PortLife', html)
        self.assertIn('Iniciar Sesión', html)
        self.assertIn('Registrarse', html)
        self.assertIn('Juan Miguel Duarte Castañeda', html)
        self.assertIn('1028140776', html)
        self.assertIn('La Estrella, Antioquia', html)
        self.assertIn('19 años', html)
        print("[OK] Test 01: Portal de inicio '/' con Registro e Inicio de Sesion verificado.")

    def test_02_portfolio_public_view(self):
        """Verifica que '/portafolio' muestre los datos de Juan Miguel Duarte y los proyectos intactos."""
        response = self.client.get('/portafolio')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        # Datos personales del estudiante
        self.assertIn('Juan Miguel Duarte Castañeda', html)
        self.assertIn('1028140776', html)
        self.assertIn('La Estrella, Antioquia', html)
        self.assertIn('19 años', html)
        self.assertIn('Ingeniería Informática', html)
        # Proyectos requeridos intactos
        self.assertIn('GlucoKids', html)
        self.assertIn('PetCare', html)
        self.assertIn('Hablemos', html)
        self.assertIn('id="contacto"', html)
        print("[OK] Test 02: Portafolio de Juan Miguel Duarte Castañeda cargado con proyectos intactos.")

    def test_03_user_registration(self):
        """Verifica el registro de un nuevo usuario en la plataforma."""
        payload = {
            "full_name": "Carlos Estudiante",
            "username": "carlos_test",
            "email": "carlos.test@correo.com",
            "password": "password123",
            "confirm_password": "password123"
        }
        res = self.client.post('/register', data=payload, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('Carlos Estudiante', html)

        with self.app.app_context():
            u = User.query.filter_by(username='carlos_test').first()
            self.assertIsNotNone(u)
            self.assertTrue(u.check_password('password123'))
            self.assertEqual(u.role, 'user')
        print("[OK] Test 03: Registro de nuevo usuario (POST /register) y hashing exitoso.")

    def test_04_user_and_admin_login(self):
        """Verifica inicio de sesión tanto de usuario registrado como de administrador."""
        # Login de usuario
        res_user = self.client.post('/login', data={'username': 'carlos_test', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(res_user.status_code, 200)

        # Logout
        self.client.get('/logout')

        # Login de administrador
        res_admin = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res_admin.status_code, 200)
        html_admin = res_admin.data.decode('utf-8')
        self.assertIn('Panel de Control', html_admin)
        print("[OK] Test 04: Inicio de sesion de usuario y administrador verificado.")

    def test_05_api_endpoints_profile_data(self):
        """Verifica que la API REST entregue los datos de Juan Miguel Duarte."""
        res_prof = self.client.get('/api/profile')
        self.assertEqual(res_prof.status_code, 200)
        profile = res_prof.get_json()
        self.assertEqual(profile['full_name'], 'Juan Miguel Duarte Castañeda')
        self.assertEqual(profile['document_id'], 'C.C 1028140776')
        self.assertEqual(profile['age'], '19 años')
        self.assertEqual(profile['location'], 'La Estrella, Antioquia')

        # Proyectos vía API
        res_proj = self.client.get('/api/projects')
        self.assertEqual(res_proj.status_code, 200)
        projects = res_proj.get_json()
        titles = [p['title'] for p in projects]
        self.assertIn('GlucoKids', titles)
        self.assertIn('PetCare', titles)
        self.assertIn('Hablemos', titles)
        print("[OK] Test 05: REST API verificada con datos actualizados y proyectos.")

    def test_06_contact_submission_and_crud(self):
        """Verifica envío de contacto y operaciones CRUD."""
        # Contacto
        payload = {
            "name": "Profesor Evaluador",
            "email": "docente@universidad.edu.co",
            "subject": "Revisión del Parcial",
            "message": "Excelente actualización con datos reales y portal de registro."
        }
        res_contact = self.client.post('/contacto', json=payload, headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(res_contact.status_code, 201)

        # Login admin para CRUD
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})

        # Crear nuevo proyecto de prueba
        res_create = self.client.post('/admin/projects/create', data={
            'title': 'Proyecto de Prueba Automatizado',
            'category': 'Prueba',
            'short_desc': 'Descripción corta',
            'full_desc': 'Descripción completa',
            'technologies': 'Python, Flask',
            'status': 'En desarrollo',
            'image_url': '/static/img/glucokids.jpg',
            'order': '99'
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)

        with self.app.app_context():
            proj = Project.query.filter_by(title='Proyecto de Prueba Automatizado').first()
            self.assertIsNotNone(proj)
            proj_id = proj.id

            # Eliminar
            self.client.post(f'/admin/projects/{proj_id}/delete', follow_redirects=True)
            self.assertIsNone(db.session.get(Project, proj_id))

        print("[OK] Test 06: Contacto y operaciones CRUD verificadas exitosamente.")

if __name__ == '__main__':
    unittest.main()
