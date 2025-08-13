from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

# Create your models here.

class Comment(models.Model):
    content = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def get_author(self):
        return self.author.get_username()
    
    def get_title(self):
        return self.post.get_title()

