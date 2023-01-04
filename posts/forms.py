from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import PostsComment, Post


class CreateCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PostsComment
        fields = ('user', 'profile', 'post', 'comment', 'parent')


class CreatePostForm(forms.ModelForm):
    # post = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ('post', 'title', 'image_header', 'draft', 'url')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'post': CKEditorUploadingWidget(),
            'image_header': forms.FileInput(attrs={'class': 'form-control'}),

        }