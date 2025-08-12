from django.db import models
from django.contrib.auth.models import User
from comments.models import Comment
 
# Create your models here.

class FeedbackComment(models.Model):
    feedback = models.BooleanField()
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbackcomments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='feedbackcomments')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_user_comment_feedback')
        ]

    def get_likes(self):
        return self.feedbackcomments.filter(feedback=True).count()
    
    def get_deslikes(self):
        return self.feedbackcomments.filter(feedback=False).count()
    
    def karma(self):
        return self.get_likes() - self.get_deslikes()
    
    def get_comment(self):
        return self.comment.content
    
    def get_user(self):
        return self.user.get_username()