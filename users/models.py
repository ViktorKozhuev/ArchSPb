from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    photo = models.ImageField(
        upload_to='users',
        blank=True,
        null=True
    )
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'slug': self.pk})
