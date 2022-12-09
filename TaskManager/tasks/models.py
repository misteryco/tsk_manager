from enum import Enum
from fileinput import filename

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from TaskManager.core.model_mixins import ChoicesEnumMixin

UserModel = get_user_model()


# def user_directory_path(instance, filename):
#     return ''.format(instance.user.username, filename)


class Priority(ChoicesEnumMixin, Enum):
    low = 'Low Priority'
    standard = 'Standard Priority'
    high = 'High Priority'


class Task(models.Model):
    NAME_MAX_LEN = 150
    NAME_MIN_LEN = 10
    name = models.CharField(
        null=False,
        blank=False,
        max_length=NAME_MAX_LEN,
        validators=[validators.MinLengthValidator(NAME_MIN_LEN, f'Name should be min {NAME_MIN_LEN} chars')]
    )

    description = models.TextField(
        null=False,
        blank=False,
    )

    due_date = models.DateField(
        null=False,
        blank=False,
    )

    priority = models.CharField(
        choices=Priority.choices(),
        max_length=Priority.max_len(),
    )

    attached_file_by_author = models.FileField(
        upload_to='',
        null=True,
        blank=True,
    )
    attached_file_by_executor = models.FileField(
        upload_to='',
        null=True,
        blank=True,
    )

    user = models.ForeignKey(UserModel,
                             on_delete=models.RESTRICT,
                             verbose_name='Assigned by:'
                             )

    executor = models.ManyToManyField(
        UserModel,
        related_name='executing_user',
    )
