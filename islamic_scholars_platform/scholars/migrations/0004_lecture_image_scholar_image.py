# Generated by Django 5.0.3 on 2024-03-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholars', '0003_alter_availability_day_of_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='scholar_images/'),
        ),
        migrations.AddField(
            model_name='scholar',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='scholar_images/'),
        ),
    ]
