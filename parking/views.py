import qrcode
from django.db.models import Count
from django.contrib import messages
from django.core.mail import send_mail
from io import BytesIO
from django.core.files import File
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from .models import ParkingSlot, Booking
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Home Page
@login_required
def home(request):
    slots = ParkingSlot.objects.all()

    for slot in slots:
        booking = Booking.objects.filter(slot=slot, end_time__isnull=True).first()
        slot.current_booking = booking

    return render(request, 'home.html', {'slots': slots})


# Book Slot
@login_required
def book_slot(request, id):
    slot = ParkingSlot.objects.get(id=id)
    if not slot.is_available:
        return redirect('/')

    # booking create
    booking = Booking.objects.create(user=request.user, slot=slot)

    # slot occupied
    slot.is_available = False
    slot.save()
    send_mail(
    "Parking Booked",
    f"Your slot is booked. Booking ID: {booking.id}",
    "test@gmail.com",
    [request.user.email],
)# QR CODE GENERATE
    qr = qrcode.make(f"Booking ID: {booking.id}")
    buffer = BytesIO()
    qr.save(buffer)
    booking.qr_code.save(f'qr_{booking.id}.png', File(buffer))

    booking.save()

    # 👇 REAL-TIME UPDATE
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "slots",
        {
            "type": "send_update",
            "data": {"msg": "updated"}
        }
    )

    return redirect('/')


# Exit Slot
@login_required
def exit_slot(request, id):
    booking = Booking.objects.get(id=id)

    booking.end_time = timezone.now()
    booking.amount = 20
    booking.save()

    booking.slot.is_available = True
    booking.slot.save()
    messages.success(request, f"Payment of ₹{booking.amount} done successfully")

    # REAL-TIME UPDATE
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "slots",
        {
            "type": "send_update",
            "data": {"msg": "updated"}
        }
    )

    return redirect('/')


@login_required
def dashboard(request):
    total_slots = ParkingSlot.objects.count()
    available_slots = ParkingSlot.objects.filter(is_available=True).count()
    occupied_slots = ParkingSlot.objects.filter(is_available=False).count()
    total_bookings = Booking.objects.count()

    return render(request, 'dashboard.html', {
        'total': total_slots,
        'available': available_slots,
        'occupied': occupied_slots,
        'bookings': total_bookings
    })