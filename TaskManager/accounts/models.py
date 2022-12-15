from enum import Enum

from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models

from TaskManager.core.model_mixins import ChoicesEnumMixin


class Role(ChoicesEnumMixin, Enum):
    engineer = 'Engineer'
    designer = 'Designer'
    manager = 'Manager'


class Level(ChoicesEnumMixin, Enum):
    team_lead = 'Team Lead'
    senior = 'Senior'
    junior = 'Junior'


class AppUser(auth_models.AbstractUser):
    FIRST_NAME_MAX_LEN = 30
    FIRST_NAME_MIN_LEN = 2
    LAST_NAME_MAX_LEN = 30
    LAST_NAME_MIN_LEN = 2

    email = models.EmailField(unique=True,  blank=False)

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=[
            validators.MinLengthValidator(FIRST_NAME_MIN_LEN, f"The name must have {FIRST_NAME_MIN_LEN} chars")]
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=[
            validators.MinLengthValidator(LAST_NAME_MIN_LEN, f"The name must be a have {LAST_NAME_MIN_LEN} chars")]
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        choices=Role.choices(),
        max_length=Role.max_len(),
    )

    level = models.CharField(
        choices=Level.choices(),
        max_length=Level.max_len(),
    )

    is_general_manager = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
