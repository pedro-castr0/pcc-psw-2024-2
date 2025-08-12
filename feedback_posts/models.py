from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
 

# Create your models here.

class FeedbackPost(models.Model):
    feedback = models.BooleanField()
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feedback_posts')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post_feedback')
        ]
    
    def get_karma(self):
        return self.get_likes() - self.get_deslikes()
    
    def get_post(self):
        return self.post.get_title()
    
    def get_user(self):
        return self.user.get_username()