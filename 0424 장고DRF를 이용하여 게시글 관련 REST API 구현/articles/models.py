from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='chch')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)