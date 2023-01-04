import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    profile = models.ForeignKey('users.Profile', on_delete=models.PROTECT)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image_header = models.ImageField(upload_to='posts', verbose_name="Иллюстрация")
    post = models.TextField(blank=True, verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    draft = models.BooleanField(default=False)
    url = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ('created',)

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.url})

    def get_comment(self):
        return self.postscomment_set.filter(parent__isnull=True)

    def __str__(self):
        return '{} by @{}'.format(self.title, self.user.username)


class PostsComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    profile = models.ForeignKey('users.Profile', on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария", blank=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Комментарий к посту"
        verbose_name_plural = "Комментарии к посту"