from django.db import models
from communities.models import Community
from django.contrib.auth.models import User
from tags.models import Tag
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    file = models.FileField(upload_to="media/post/files", blank=True, null=True)
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True, blank=True, null=True)
    post_tag = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.__class__.__name__

    def get_author(self):
        return self.author.get_username()
    
    def get_community(self):
        return self.community.get_name()
    
    def get_title(self):
        return self.title
    
    def get_likes(self):
        from feedback.models import Feedback
        return Feedback.objects.filter(post=self, feedback=True).count()
    
    def get_dislikes(self):
        from feedback.models import Feedback
        return Feedback.objects.filter(post=self, feedback=False).count()
    
    def get_karma(self):
        return self.get_likes() - self.get_dislikes()

    def get_comments_count(self):
        from comments.models import Comment
        return Comment.objects.filter(post=self).count()
    
    def get_comments(self):
        from comments.models import Comment
        return Comment.objects.filter(post=self)
    
    def get_absolute_url(self):
        return reverse('view', kwargs={'id': self.id})