from django.db import models
from django.contrib.auth.models import User
from follows.models import Follow
from django import template


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=20)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)

    register = template.Library()
    
    @register.simple_tag
    def is_following(follower, followed):
        return Follow.objects.filter(follower=follower, followed=followed).exists()