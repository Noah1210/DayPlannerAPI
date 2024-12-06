from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from dayplanner.models import User, Task, Note, Todo


class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {self.token.key}"}
    
        now = timezone.now()


        self.event = Task.objects.create(
            id=1, 
            user=self.user,
            title="Sample Event",
            date_start=now,
            date_end=now + timedelta(hours=1),
            color="#FFFFFF", 
        )
        self.note = Note.objects.create(
            user=self.user, content="Sample Note", date=now
        )
        self.todo = Todo.objects.create(user=self.user, title="Sample Todo", date=now, is_done=False, is_priority=False)

    def test_registration_success(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
        }
        response = self.client.post("/api/register/", data=data)  
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("token", response_data)

    def test_registration_duplicate_email(self):
        data = {
            "username": "anotheruser",
            "email": self.user.email,  
            "password": "password123",
        }
        response = self.client.post("/api/register/", data=data)  
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["error"], "Email already in use")

    def test_login_success(self):
        data = {"email": self.user.email, "password": "password123"}
        response = self.client.post("/api/login/", data=data) 
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("token", response_data)

    def test_login_invalid_credentials(self):
        data = {"email": self.user.email, "password": "wrongpassword"}
        response = self.client.post("/api/login/", data=data) 
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Invalid email or password")   

    def test_logout_success(self):
        self.client.login(username="testuser", email="test@example.com", password="password123")
        response = self.client.post("/api/logout/", **self.auth_header)  
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_event_get_all(self):
        date_query = timezone.now().date()
        response = self.client.get(f"/api/event/?date={date_query}", **self.auth_header)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "events retrieved successfully")

    def test_event_create(self):
        data = {
            "title": "New Event",
            "date_start": timezone.now(),
            "date_end": timezone.now() + timedelta(hours=2),
            "color": "#FF5733",
        }
        response = self.client.post("/api/event/", data=data, **self.auth_header) 
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Event created successfully")

    def test_event_update(self):
        data = {"title": "Updated Event", "date_start": timezone.now(), "date_end": timezone.now() + timedelta(hours=2), "color": "#FF5833"}
        response = self.client.put(
            f"/api/event/{self.event.id}", data=data, **self.auth_header
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "event updated successfully")

    def test_event_delete(self):
        response = self.client.delete(f"/api/event/{self.event.id}", **self.auth_header)  
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "event deleted successfully")

    def test_note_get(self):
        date_query = timezone.now().date()
        response = self.client.get(f"/api/note/?date={date_query}", **self.auth_header)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Notes retrieved successfully")

    def test_note_create(self):
        data = {"content": "New Note", "date": timezone.now().date()}
        response = self.client.post("/api/note/", data=data, **self.auth_header) 
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Note created successfully")

    def test_todo_get(self):
        date_query = "2024-06-13"
        response = self.client.get(f"/api/task/?date={date_query}", **self.auth_header)  
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        tasks = response_data['response']
        
        self.assertIsInstance(tasks, list)
        
        for task in tasks:
            self.assertIn('id', task)
            self.assertIn('title', task)
            self.assertIn('date', task)
            self.assertIn('is_done', task)
            self.assertIn('is_priority', task)
        
        for task in tasks:
            self.assertEqual(task['date'], date_query)

    def test_todo_create(self):
        data = {"title": "New Todo", "date": timezone.now().date(), "is_done": False, "is_priority": False}
        response = self.client.post("/api/task/", data=data, **self.auth_header)  
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Task created successfully")
