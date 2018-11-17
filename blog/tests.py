from rest_framework import status
from django.test import TestCase, override_settings, modify_settings

from rest_framework.test import APIClient


class BlogTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @override_settings(MIDDLEWARE=[
        'blog.middleware.IndexMiddleware'
    ], DEBUG=True)
    def test_create_blog(self):
        response = self.client.post('/api/blogs/', {
            "site": "example.com",
            "description": "Example blog site"
        }, format='json')

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
