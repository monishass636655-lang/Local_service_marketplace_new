from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class ProviderProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    services = models.ManyToManyField('services.Service')

    experience = models.IntegerField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username