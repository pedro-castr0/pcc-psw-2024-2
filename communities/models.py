from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag

class Community(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=20)
    context = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='communities')
    created = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities')
    community_picture = models.ImageField(upload_to='community/pics/', blank=True, null=True)
    community_banner = models.ImageField(upload_to='community/banners/', blank=True, null=True)

    def get_name(self):
        return self.name

    def get_creator(self):
        return self.creator.get_username()    
    
    def get_tags(self):
        return self.tags.all()
    
    @staticmethod
    def search_by_tag(tag_name):
        """Retorna todas as comunidades que possuem a tag com o nome dado"""
        return Community.objects.filter(tags__name__iexact=tag_name)
