# forms.py
from django import forms
from .models import Comment

class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'post', 'parent']
