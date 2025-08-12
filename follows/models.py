from django.db import models
from django.contrib.auth.models import User
 
# Create your models here.

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followed', 'follower'], name='unique_followed_follower_follow')
        ]
    
    def get_followed(self):
        return self.followed.get_username()
    
    def get_follower(self):
        return self.follower.get_username()
