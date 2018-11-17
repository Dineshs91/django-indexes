from django.urls import path, re_path, include

from blog.views import BlogView


urlpatterns = [
    path("blogs/<int:blog_id>/", BlogView.as_view())
]
