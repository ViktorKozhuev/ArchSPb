# Generated by Django 4.1.3 on 2022-11-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='architect',
            name='description',
            field=models.TextField(default='Описание', verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='archstyle',
            name='description',
            field=models.TextField(default='Описание', verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='Описание', verbose_name='Описание'),
        ),
    ]
