from django.db import models
from django.contrib.auth.models import User
from communities.models import Community

class Join(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_communities')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['community', 'user'], name='unique_community_user_follow')
        ]
    
    def get_community(self):
        return self.community.get_name()
    
    def get_user(self):
        return self.user.get_username()