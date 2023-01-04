from django import forms
# Models
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(forms.Form):

    email = forms.CharField(
        min_length=4,
        max_length=70,
        widget=forms.EmailInput()
    )
    username = forms.CharField(
        min_length=4,
        max_length=70,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    def clean(self):

        data = super().clean()
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise forms.ValidationError('Пароли не совпадают.')
        return data

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

