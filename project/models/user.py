from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from project.tasks import send_installation_fee_paid_mail
# Create your models here.


class User(AbstractUser):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=35, blank=True, null=True)
    state = models.CharField(max_length=35, blank=True, null=True)
    is_organization = models.BooleanField(default=False)
    is_ordinary = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    paid_installment_fee = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.username}"

    def installation_fee_paid(self):
        self.paid_installment_fee = True
        self.save()
        send_installation_fee_paid_mail.delay(self.id)
        return True