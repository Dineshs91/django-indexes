from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from blog.models import Blog
from blog.serializers import BlogSerializer
from utils.common import create_response


class BlogView(APIView):
    def post(self, request):
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return create_response(data=serializer.data, status=status.HTTP_201_CREATED)
        return create_response(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, blog_id=None):
        if blog_id is None:
            blogs = Blog.objects.all()
            serializer = BlogSerializer(blogs, many=True)
            return create_response(data=serializer.data, status=status.HTTP_200_OK)

        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return create_response(error={"message": "Blog does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlogSerializer(blog)
        return create_response(data=serializer.data, status=status.HTTP_200_OK)
