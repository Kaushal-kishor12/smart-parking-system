
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Parking Slot Model
class ParkingSlot(models.Model):
    slot_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.slot_number


# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    amount = models.FloatField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.slot.slot_number}"
    
    