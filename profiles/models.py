from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    display_name = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile/pics/', blank=True, null=True)
    profile_banner = models.ImageField(upload_to='profile/banners/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

def create_profile(sender, instance, created, **kwards):
    if created:
        profile = Profile.objects.create(
            user=instance,
            display_name=instance.username
            )
        profile.save()

post_save.connect(create_profile, sender=User)