# Generated by Django 3.0.7 on 2020-07-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200718_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='sample-slug', unique=False),
        ),
    ]
