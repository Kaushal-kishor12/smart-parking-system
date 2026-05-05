from django.contrib import admin
from .models import ParkingSlot, Booking

class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'is_available')  # 👈 ये important

admin.site.register(ParkingSlot, ParkingSlotAdmin)
admin.site.register(Booking)