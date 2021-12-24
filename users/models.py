import uuid
import pyotp

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    CustomUser extending the AbstractUser to add is_verified field for authentication
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=32, default=pyotp.random_base32)

    def __str__(self):
        return self.username

    def get_otp(self):
        """
        Method for OTP generation and handling
        """
        totp = pyotp.TOTP(self.secret_key, digits=4, interval=60)
        return totp.now()

    def verify_otp(self, user_input):
        """
        Class method to verify passed otp
        """
        totp = pyotp.TOTP(self.secret_key, digits=4, interval=60)
        self.is_verified = totp.verify(user_input)
        self.save()
        return self.is_verified
