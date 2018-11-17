from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from blog.models import Blog
from blog.serializers import BlogSerializer


class BlogView(APIView):
    def post(self, request):
        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response(data={"error": "Blog does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlogSerializer(blog)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
