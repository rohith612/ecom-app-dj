# Generated by Django 3.0.7 on 2020-07-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='cat_new.jpg', null=True, upload_to=''),
        ),
    ]
