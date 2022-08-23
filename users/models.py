from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    total_storage = models.CharField(max_length=500, default=60000)
    used_storage = models.CharField(max_length=500, default=0)
