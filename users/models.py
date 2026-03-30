from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)      

    objects= CustomUserManager()
      
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    def __str__(self):
        return self.email

        
        
        
class ConfirmationCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"код подтверждение для {self.user.email}"