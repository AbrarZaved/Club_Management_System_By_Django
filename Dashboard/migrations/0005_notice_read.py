# Generated by Django 5.0.4 on 2024-08-02 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0004_notice_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
