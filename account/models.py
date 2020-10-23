from cities_light.models import Region
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models


class User(AbstractUser):
    deleted_in = models.DateField(auto_now=False, auto_now_add=False,
                                  null=True, blank=True)
    is_deleted = models.BooleanField(null=False, default=False)

    class Meta:

        db_table = "user"

    @property
    def profile(self):
        if self.is_superuser:
            return "superuser"
        
        profiles = ["client", "architecture"]
        
        for profile in profiles:
            if hasattr(self, profile):
                return profile
        return None
    
    def __str__(self):
        return self.get_short_name()
        
    def clean(self):
        if not self.first_name:
            raise ValidationError({"first_name": "First name must be filled."})

        if not self.last_name:
            raise ValidationError({"last_name": "Last name must be filled."})

        if not self.email:
            raise ValidationError({"email": "Email must be filled."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        

class Architecture(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True, default=None
    )

    class Meta:
        db_table = "architecture"

    def __str__(self):
        return self.user


class Client(models.Model):

    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    birthday = models.DateField(auto_now=False, auto_now_add=False,
                                blank=True, null=True)
    gender = models.CharField(max_length=2, choices=CHOICES, blank=False,
                              null=False)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        default=None
    )
    region = models.ForeignKey(Region, on_delete=models.SET_NULL,
                               related_name='clients',
                               blank=True,
                               null=True)

    class Meta:
        db_table = "client"

    def __str__(self):
        return self.user.first_name


