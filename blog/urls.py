from django.urls import path, re_path, include

from blog.views import BlogView


urlpatterns = [
    path("blogs/", BlogView.as_view())
]
