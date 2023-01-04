import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание", default='Описание')
    url = models.SlugField(max_length=20, unique=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_url': self.url})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Archstyle(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Стиль")
    description = models.TextField("Описание", default='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('archstyle', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стили'


class Street(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Улица")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('street', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'


class Architect(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name="Архитектор")
    description = models.TextField("Описание", default='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    image = models.ImageField("Изображение", upload_to='architects/', null=True, blank=True )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('architect', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Архитектор'
        verbose_name_plural = 'Архитекторы'
        ordering = ['name']


class Building(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image = models.ImageField("Изображение", upload_to='buildings/')
    text = models.TextField("Описание")
    year = models.PositiveSmallIntegerField("Дата постройки", default=None, null=True, blank=True)
    street = models.ManyToManyField(Street, verbose_name='Улица', related_name='building_street', blank=True)
    housenumber = models.PositiveSmallIntegerField("Номер дома", default=1)
    letter = models.CharField(max_length=8, verbose_name="Литера", null=True, blank=True)
    architect = models.ManyToManyField(Architect, verbose_name='Архитектор', related_name='building_architect', blank=True)
    archstyle = models.ForeignKey(Archstyle, verbose_name='Стиль', related_name='building_archstyle', blank=True, on_delete=models.PROTECT, null=True)
    category = models.ForeignKey(Category,  verbose_name='Категория', related_name='building_archstyle', blank=True, on_delete=models.PROTECT, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    lat = models.FloatField(verbose_name='широта', help_text='указать широту в градусах', null=True, blank=True)
    lag = models.FloatField(verbose_name='долгота', help_text='указать долготу в градусах', null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('building_detail', kwargs={'slug': self.url})

    def get_comment(self):
        return self.buildingcomment_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Здание"
        verbose_name_plural = "Здания"


class BuildingImages(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='buildings_images/')
    movie = models.ForeignKey(Building, verbose_name='Здание', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class BuildingComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    profile = models.ForeignKey('users.Profile', on_delete=models.PROTECT, related_name='profile')
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария", blank=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


