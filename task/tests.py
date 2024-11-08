from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class TaskTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Crear un usuario superadministrador
        user_class = get_user_model()
        cls.user = get_user_model().objects.create_superuser(
            username="test@example.com", password="testpassword"
        )
        
        # Generar el token de acceso JWT para el usuario
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)

        # Crear tareas para las pruebas
        cls.task = Task.objects.create(
            title="Test Task 1",
            description="This is a test task",
            user=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        cls.task.delete()
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        # Configurar los encabezados de autenticación
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_task_str(self):
        """Prueba para el método __str__ de Task"""
        expected_str = "Test Task 1"
        self.assertEqual(str(self.task), expected_str)

    def test_get_task_list(self):
        url = reverse("task-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Asegura que hay al menos una tarea

    def test_get_task_detail(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_create_task(self):
        url = reverse("task-list")
        data = {
            "title": "New Task",
            "description": "A description for a new task."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])

    def test_update_task(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        data = {
            "title": "Updated Task",
            "description": "Updated description"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])

    def test_partial_update_task(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        data = {"description": "Partial updated description"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], data["description"])

    def test_delete_task(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# Create your tests here.
