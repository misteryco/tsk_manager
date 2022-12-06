# Generated by Django 4.1.3 on 2022-12-06 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0006_alter_task_attached_file_by_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_comment', models.CharField(blank=True, max_length=255)),
                ('comment_date_and_time', models.DateTimeField(auto_now_add=True)),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('commented_section', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='ShortNewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_article', models.CharField(max_length=300)),
                ('date_and_time_of_article', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_comment', models.CharField(blank=True, max_length=255)),
                ('comment_date_and_time', models.DateTimeField(auto_now_add=True)),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('commented_section', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='common.shortnewsarticle')),
            ],
        ),
    ]
