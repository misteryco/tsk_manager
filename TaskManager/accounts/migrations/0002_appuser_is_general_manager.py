# Generated by Django 4.1.3 on 2022-11-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_general_manager',
            field=models.BooleanField(default=False),
        ),
    ]