# Generated by Django 4.2.6 on 2023-10-30 14:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_exam_exam_availabilty'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='joinedcohort',
            unique_together={('cohort', 'user')},
        ),
    ]