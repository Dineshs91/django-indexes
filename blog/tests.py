from rest_framework import status
from django.test import TestCase, override_settings, modify_settings

from rest_framework.test import APIClient

from blog.models import Blog, Post


class BlogTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        blog = Blog.objects.create(
            site="sample.com",
            description="Sample blog site"
        )

        Post.objects.create(
            blog=blog,
            title='post title',
            content='post content'
        )

    @override_settings(MIDDLEWARE=[
        'core.middleware.IndexMiddleware'
    ], DEBUG=True)
    def test_create_blog(self):
        response = self.client.post('/api/blogs/', {
            "site": "example.com",
            "description": "Example blog site"
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(MIDDLEWARE=[
        'core.middleware.IndexMiddleware'
    ], DEBUG=True)
    def test_get_blog(self):
        blog_id = Blog.objects.get(site="sample.com").id
        response = self.client.get('/api/blogs/{}/'.format(blog_id), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(MIDDLEWARE=[
        'core.middleware.IndexMiddleware'
    ], DEBUG=True)
    def test_get_post(self):
        blog_id = Blog.objects.get(site="sample.com").id
        post_id = Post.objects.get(title="post title").id

        response = self.client.get('/api/blogs/{}/posts/{}/'.format(blog_id, post_id), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(MIDDLEWARE=[
        'core.middleware.IndexMiddleware'
    ], DEBUG=True)
    def test_get_blog_by_site(self):
        blog_site = "sample.com"

        response = self.client.get('/api/blogs/{}/'.format(blog_site), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(MIDDLEWARE=[
        'core.middleware.IndexMiddleware'
    ], DEBUG=True)
    def test_get_blog_by_site_from_post(self):
        blog_site = "sample.com"

        response = self.client.get('/api/blogs/{}/posts/'.format(blog_site), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
