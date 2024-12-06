from rest_framework.test import APIClient, APITestCase
from dayplanner.models import User, Task

class IntegrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)  

    def test_event_creation_and_retrieval(self):
        event_data = {
            "title": "Test event",
            "date_start": "2024-12-06T09:00:00Z",
            "date_end": "2024-12-06T10:00:00Z",
            "color": "#FF0000",
        }
        response = self.client.post("/api/event/", data=event_data, format="json")
        self.assertEqual(response.status_code, 201)
        event_date_start = response.json()["date_start"]
        event_date = event_date_start.split("T")[0]
        
        response = self.client.get(f"/api/event/?date={event_date}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["response"][0]["title"], "Test event")
        
        event_id = response.json()["response"][0]["id"]
        response = self.client.delete(f"/api/event/{event_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "event deleted successfully")
        
    def test_full_auth_cycle(self):
        user_data = {
            "username": "newuser",
            "email": "newuser@gmail.com",
            "password": "password123",
        }
        response = self.client.post("/api/register/", data=user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        token = response.json()["token"]
        
    def test_full_auth_cycle(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
        }
        response = self.client.post("/api/register/", data=data)  
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        token = response.json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}") 
        event_date = "2024-12-06"
        response = self.client.get(f"/api/event/?date={event_date}")
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/api/logout/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Logout successful")
        self.client.logout()
        
        event_date = "2024-12-06"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(f"/api/event/?date={event_date}")
        self.assertEqual(response.status_code, 401)
