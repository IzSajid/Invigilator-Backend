# Generated by Django 4.2.6 on 2023-10-30 13:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='exam_availabilty',
            field=models.DurationField(default=datetime.timedelta(days=1)),
        ),
    ]
