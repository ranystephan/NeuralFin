from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient

from .models import User

client = APIClient()

response = client.post('/register/', {'name': 'John Doe', 'email': 'john@example.com', 'password': 'password123'})
assert response.status_code == 200


response = client.post('/login/', {'email': 'john@example.com', 'password': 'password123'})
assert response.status_code == 200
access_token = response.data['jwt']


client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
response = client.put('/update_profile/', {'username': 'new_username', 'email': 'new_email@example.com'}, format='json')
assert response.status_code == 200
