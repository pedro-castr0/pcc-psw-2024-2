from django.contrib import admin
from comments.models import Comment
from posts.models import Post
from tags.models import Tag

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Tag)
# Register your models here.
