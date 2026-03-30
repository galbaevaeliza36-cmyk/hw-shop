from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone_number=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

       
        if not phone_number:
            raise ValueError("Суперпользователь должен иметь phone_number")

        return self.create_user(email, phone_number, password, **extra_fields)