from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=20)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)

def create_profile(sender, instance, created, **kwards):
    if created:
        profile = Profile.objects.create(
            user=instance,
            display_name=instance.username
            )
        profile.save()

post_save.connect(create_profile, sender=User)