from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient


class BlogTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_blog(self):
        response = self.client.post('/api/blogs/', {
            "site": "example.com",
            "description": "Example blog site"
        }, format='json')

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        print(response.json())
