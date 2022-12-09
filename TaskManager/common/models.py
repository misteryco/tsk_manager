from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

from TaskManager.tasks.models import Task

UserModel = get_user_model()


class ShortNewsArticle(models.Model):
    MAX_TEXT_TITLE_LEN = 40
    MAX_TEXT_LEN = 300

    news_Title = models.CharField(
        max_length=MAX_TEXT_TITLE_LEN,
        null=False,
        blank=False,
    )
    news_article = models.CharField(
        max_length=MAX_TEXT_LEN,
        null=False,
        blank=False,
    )

    date_and_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return f'{self.news_Title} by {self.user}'


class TaskComment(models.Model):
    MAX_TEXT_LEN = 255

    task_comment = models.CharField(
        max_length=MAX_TEXT_LEN,
        null=False,
        blank=True,
    )

    commented_section = models.ForeignKey(
        Task,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    date_and_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )
    comment_user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )


class NewsComment(models.Model):
    MAX_TEXT_LEN = 255

    news_comment = models.CharField(
        max_length=MAX_TEXT_LEN,
        null=False,
        blank=True,
    )

    commented_section = models.ForeignKey(
        ShortNewsArticle,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    date_and_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
    )

    comment_user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )
