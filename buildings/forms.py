from django import forms

from .models import BuildingComment


from django.contrib.auth.models import User


class CreateCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = BuildingComment
        fields = ('user', 'profile', 'building', 'comment', 'parent')
