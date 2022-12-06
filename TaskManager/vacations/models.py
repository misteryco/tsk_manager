from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Vacation(models.Model):
    start_date = models.DateField(
        null=False,
        blank=False,
    )
    end_date = models.DateField(
        null=False,
        blank=False)

    created_on = models.DateField(
        auto_now=True,
        blank=True,
        null=False)

    approved = models.BooleanField(
        default=False,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )
