from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from blog.models import Blog, Post
from utils.common import create_response
from blog.serializers import BlogSerializer, PostSerializer


class BlogListView(APIView):
    def post(self, request):
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return create_response(data=serializer.data, status=status.HTTP_201_CREATED)
        return create_response(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return create_response(data=serializer.data, status=status.HTTP_200_OK)


class BlogDetailView(APIView):
    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return create_response(error={"message": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return create_response(data=serializer.data, status=status.HTTP_200_OK)


class BlogSiteView(APIView):
    def get(self, request, site):
        try:
            blog = Blog.objects.get(site=site)
        except Blog.DoesNotExist:
            return create_response(error={"message": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return create_response(data=serializer.data, status=status.HTTP_200_OK)

class PostView(APIView):
    def get(self, request, blog_id, post_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return create_response(error={"message": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = blog.blog_posts.get(id=post_id)
        except Post.DoesNotExist:
            return create_response(error={"message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return create_response(data=serializer.data, status=status.HTTP_200_OK)
