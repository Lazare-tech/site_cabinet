from django.db import models
from django.contrib.auth.models import AbstractUser
import os

from django.utils import timezone
from datetime import timedelta


# Create your models here.
class User(AbstractUser):
    pass