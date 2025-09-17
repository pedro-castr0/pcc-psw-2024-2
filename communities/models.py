from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    display_name = models.CharField(max_length=20)
    context = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    community_picture = models.ImageField(upload_to='community/pics/', blank=True, null=True)
    community_banner = models.ImageField(upload_to='community/banners/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities')
    
    def __str__(self):
        return self.__class__.__name__

    def get_name(self):
        return self.name or self.display_name

    def get_creator(self):
        return self.creator.get_username()
    
    @staticmethod
    def search_by_tag(tag_name):
        return Community.objects.filter(community_tags__name__iexact=tag_name)

class CommunityRule(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="rules"
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.community.get_name()} - {self.title}"
