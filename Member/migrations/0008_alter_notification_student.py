# Generated by Django 5.0.4 on 2024-08-02 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0007_remove_notification_student_notification_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='student',
            field=models.ManyToManyField(to='Member.memberjoined', verbose_name='Students'),
        ),
    ]
