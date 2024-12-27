from django.utils.timezone import now
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Account"

    def generate_otp(self):
        import pyotp
        otp = pyotp.random_base32()[:6]
        self.otp = otp
        self.otp_expiry = now() + timedelta(minutes=2)  # OTP valid for 2 minutes
        self.save()
        return otp