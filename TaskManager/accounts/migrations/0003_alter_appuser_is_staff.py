# Generated by Django 4.1.3 on 2022-12-06 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_appuser_is_general_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]