from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities')

    def get_name(self):
        return self.name

    def get_creator(self):
        return self.creator.get_username()
