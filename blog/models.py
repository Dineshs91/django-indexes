from django.db import models


class Blog(models.Model):
    site = models.CharField(max_length=100)
    description = models.CharField(max_length=255)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=100, db_column='post_title')
    content = models.TextField()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    content = models.TextField()
