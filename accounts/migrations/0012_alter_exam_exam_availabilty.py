# Generated by Django 4.2.6 on 2023-11-16 19:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_exam_exam_availabilty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_availabilty',
            field=models.DurationField(default=datetime.timedelta(days=1)),
        ),
    ]