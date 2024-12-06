from django.test import TestCase
from rest_framework.exceptions import ValidationError
from dayplanner.models import User, Task
from dayplanner.serializers import EventSerializer

class TestSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.task = Task.objects.create(
            user=self.user,
            title="Sample event",
            date_start="2024-6-05T10:00:00Z",
            date_end="2024-6-05T12:00:00Z",
            color="#FFFFFF"
        )

    def test_event_serializer_valid(self):
        serializer = EventSerializer(self.task)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Sample event')
        self.assertEqual(data['color'], '#FFFFFF')
        self.assertIn('date_start', data)
        self.assertIn('date_end', data)

    def test_event_serializer_invalid(self):
        invalid_data = {
            'title': '',  # Invalid because the title is required
            'color': '#FFFFFF',
            'user': self.user.id,
            'date_start': '2024-6-05T10:00:00Z',
            'date_end': '2024-6-05T12:00:00Z'
        }
        
        serializer = EventSerializer(data=invalid_data)
        
        # Check if serializer catches the validation error
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_event_deserialization_valid(self):
        data = {
            'title': 'New event',
            'color': '#FF5733',
            'date_start': '2024-12-06T09:00:00Z',
            'date_end': '2024-12-06T11:00:00Z'
        }
        
        serializer = EventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        self.assertEqual(serializer.validated_data['title'], 'New event')
        self.assertEqual(serializer.validated_data['color'], '#FF5733')

    def test_event_deserialization_invalid(self):
        invalid_data = {
            'title': 'New event',  
            'color': '#FF5733',
            'date_end': '2024-12-06T11:00:00Z'
        }
        
        serializer = EventSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('date_start', serializer.errors)
