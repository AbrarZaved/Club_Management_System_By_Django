# Generated by Django 5.0.4 on 2024-08-02 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0006_alter_notification_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='student',
        ),
        migrations.AddField(
            model_name='notification',
            name='student',
            field=models.ManyToManyField(null=True, to='Member.memberjoined', verbose_name='Students'),
        ),
    ]