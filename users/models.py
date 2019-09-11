from django.db import models


class Users(models.Model):
    """User model."""

    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    email_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

class ActivationToken(models.Model):
    """Email Activation model."""
    owner=models.OneToOneField(Users, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=255, unique=True)
    expiry_at = models.CharField(max_length=255)
    class Meta:
        db_table = 'activation_token'
    
    def __str__(self):
        return self.activation_token

class PasswordResetToken(models.Model):
    """Password Reset model."""
    owner=models.OneToOneField(Users, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=255, unique=True)
    expiry_at = models.CharField(max_length=255)
    class Meta:
        db_table = 'reset_token'
    
    def __str__(self):
        return self.reset_token