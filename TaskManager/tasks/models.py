from datetime import date
from enum import Enum

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from TaskManager.core.model_mixins import ChoicesEnumMixin
from TaskManager.core.validators import max_file_size_in_five_mb_validator

UserModel = get_user_model()


class Priority(ChoicesEnumMixin, Enum):
    low = 'Low Priority'
    standard = 'Standard Priority'
    high = 'High Priority'


class Task(models.Model):
    NAME_MAX_LEN = 50
    NAME_MIN_LEN = 10
    DESCR_MAX_LEN = 50

    name = models.CharField(
        null=False,
        blank=False,
        max_length=NAME_MAX_LEN,
        validators=[validators.MinLengthValidator(NAME_MIN_LEN, f'Name should be min {NAME_MIN_LEN} chars'), ],
    )

    description = models.TextField(
        null=False,
        blank=False,
        validators=[validators.MaxLengthValidator(DESCR_MAX_LEN, f'Description should be max {DESCR_MAX_LEN} chars'), ],
    )

    due_date = models.DateField(
        null=False,
        blank=False,
        validators=[validators.MinValueValidator(date.today(), f'Task due date cannot be in the past !')]
    )

    priority = models.CharField(
        choices=Priority.choices(),
        max_length=Priority.max_len(),
    )

    attached_file_by_author = models.FileField(
        upload_to='uploads/',
        null=True,
        blank=True,
        validators=[max_file_size_in_five_mb_validator, ],
    )
    attached_file_by_executor = models.FileField(
        upload_to='uploads/',
        null=True,
        blank=True,
        validators=[max_file_size_in_five_mb_validator, ],
    )

    user = models.ForeignKey(UserModel,
                             on_delete=models.RESTRICT,
                             verbose_name='Assigned by:'
                             )

    executor = models.ManyToManyField(
        UserModel,
        related_name='executing_user',
    )
