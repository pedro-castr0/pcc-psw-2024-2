from django.db import models
from communities.models import Community
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    tag = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')

    def get_author(self):
        return self.author.get_username()
    
    def get_community(self):
        return self.community.get_name()
    
    def get_title(self):
        return self.title
    
    def get_likes(self):
        from feedback_posts.models import FeedbackPost
        return FeedbackPost.objects.filter(post=self, feedback=True).count()
    
    def get_dislikes(self):
        from feedback_posts.models import FeedbackPost
        return FeedbackPost.objects.filter(post=self, feedback=False).count()

    def get_comments_count(self):
        from comments.models import Comment
        return Comment.objects.filter(post=self).count()
    
    def get_comments(self):
        from comments.models import Comment
        return Comment.objects.filter(post=self)