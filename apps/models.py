from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User 



class Flight(models.Model):
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class_type = models.CharField(max_length=20)
    total_seat = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.airline} - {self.flight_number}"

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True,default=1) 
    departure_date = models.DateField(null=True)
    class_type = models.CharField(max_length=50,null=True)
    flight_fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking ID: {self.pk}, {self.departure_date} - {self.flight}"




class Payment(models.Model):
    STATUS_CHOICES = [
        ('fail', 'Fail'),
        ('pass', 'Pass'),
    ]

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid = models.CharField(max_length=10, choices=STATUS_CHOICES, default='fail')

    def __str__(self):
        return f"Payment for Booking {self.booking_id}: {self.reference}"


class Passenger(models.Model):
    booking = models.ForeignKey(
        'Booking',
        related_name='passengers',
        on_delete=models.CASCADE
    )
    flight_id = models.IntegerField(null=True)
    name = models.CharField(
        _('Name'),
        max_length=100,
        null=True,
        blank=True
    )
    age = models.IntegerField(
        _('Age'),
        null=True,
        blank=True
    )
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],null=True)
    contact_number = models.CharField(
        _('Contact Number'),
        max_length=20,
        default='2122112'
    )
    email = models.EmailField(
        _('Email'),
        default='noreply@example.com'
    )
    seat = models.CharField(max_length=3,null=True)


    def __str__(self):
        return f'{self.name} - Booking ID: {self.booking_id}'
    

