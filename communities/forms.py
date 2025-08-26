from django import forms
from .models import CommunityRule

class CommunityRuleForm(forms.ModelForm):
    class Meta:
        model = CommunityRule
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }