from django.urls import path

from blog.views import BlogListView, BlogDetailView, PostView, BlogSiteView, BlogPostView


urlpatterns = [
    path("blogs/", BlogListView.as_view()),
    path("blogs/<int:blog_id>/", BlogDetailView.as_view()),
    path("blogs/<str:site>/", BlogSiteView.as_view()),
    path("blogs/<int:blog_id>/posts/<int:post_id>/", PostView.as_view()),
    path("blogs/<str:site>/posts/", BlogPostView.as_view())
]
