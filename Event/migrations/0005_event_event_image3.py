# Generated by Django 5.1 on 2024-11-12 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0004_rename_event_image_event_event_image1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_image3',
            field=models.ImageField(blank=True, default='profile_pic/new_logo.png', upload_to='event_image'),
        ),
    ]