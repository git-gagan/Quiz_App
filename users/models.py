from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    CustomUser extending the AbstractUser to add is_verified field for authentication
    """
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
