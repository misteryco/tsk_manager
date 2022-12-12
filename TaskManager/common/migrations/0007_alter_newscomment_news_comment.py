# Generated by Django 4.1.3 on 2022-12-10 11:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_alter_newscomment_news_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newscomment',
            name='news_comment',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1, 'Comment should have at least1 char.')]),
        ),
    ]
