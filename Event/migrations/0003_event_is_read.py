# Generated by Django 5.1 on 2024-11-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0002_event_created_at_event_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_read',
            field=models.BooleanField(default=False, verbose_name='Read'),
        ),
    ]
