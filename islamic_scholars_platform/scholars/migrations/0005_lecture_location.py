# Generated by Django 5.0.3 on 2024-03-24 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholars', '0004_lecture_image_scholar_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='location',
            field=models.CharField(default='"', max_length=100),
            preserve_default=False,
        ),
    ]