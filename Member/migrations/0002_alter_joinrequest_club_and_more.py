# Generated by Django 5.0.4 on 2024-06-23 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_alter_club_tag'),
        ('Member', '0001_initial'),
        ('authentication', '0005_alter_student_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinrequest',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dashboard.club'),
        ),
        migrations.AlterUniqueTogether(
            name='joinrequest',
            unique_together={('student', 'club')},
        ),
    ]
