from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from services.models import Service


class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_bookings'
    )

    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_bookings'
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    date = models.DateField()

    time = models.TimeField()

    PAYMENT_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='unpaid'
    )

    def __str__(self):
        return f"{self.customer} - {self.service}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('booking_created', 'Booking Created'),
        ('booking_accepted', 'Booking Accepted'),
        ('booking_completed', 'Booking Completed'),
        ('payment_success', 'Payment Successful'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"