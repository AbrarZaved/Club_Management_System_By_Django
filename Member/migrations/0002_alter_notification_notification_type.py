# Generated by Django 5.0.4 on 2024-07-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('join_request', 'Join Request'), ('events', 'Events'), ('notices', 'Notices')], max_length=100),
        ),
    ]
