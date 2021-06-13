from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=35, blank=True, null=True)
    state = models.CharField(max_length=35, blank=True, null=True)
    is_organization = models.BooleanField(default=False)
    is_ordinary = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.username}"