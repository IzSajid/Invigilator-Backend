# Generated by Django 4.2.6 on 2023-11-14 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_mcq'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerMCQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_option', models.CharField(max_length=50)),
                ('mcq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.mcq')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]