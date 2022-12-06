# Generated by Django 4.1.3 on 2022-11-23 14:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_remove_task_executor_task_executor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ManyToManyField(related_name='executing_user', to=settings.AUTH_USER_MODEL),
        ),
    ]