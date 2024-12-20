# Generated by Django 5.1 on 2024-11-09 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Dashboard', '0007_alter_notice_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField()),
                ('event_location', models.CharField(max_length=100)),
                ('event_description', models.TextField()),
                ('event_image', models.ImageField(blank=True, default='profile_pic/new_logo.png', upload_to='event_image')),
                ('event_link', models.URLField()),
                ('event_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.club', verbose_name='Club')),
            ],
        ),
    ]
