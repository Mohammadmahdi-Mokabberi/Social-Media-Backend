# Generated by Django 4.0.6 on 2022-07-28 20:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_posts_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='user_liked', to=settings.AUTH_USER_MODEL, verbose_name='لایک'),
        ),
    ]
