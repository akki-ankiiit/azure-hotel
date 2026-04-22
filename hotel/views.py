from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Guest, Room


def dashboard(request):
    """Main dashboard – list of all bookings."""
    bookings = Booking.objects.select_related('guest', 'room').order_by('-created_at')
    rooms = Room.objects.all()
    guests = Guest.objects.all()
    context = {
        'bookings': bookings,
        'rooms': rooms,
        'guests': guests,
        'total_bookings': bookings.count(),
        'confirmed_bookings': bookings.filter(status='Confirmed').count(),
        'total_rooms': rooms.count(),
        'occupied_rooms': Room.objects.filter(is_available=False).count(),
        'total_guests': guests.count(),
        'checked_in': bookings.filter(status='Checked-In').count(),
    }
    return render(request, 'hotel/dashboard.html', context)


def guest_profile(request, guest_id):
    """Guest profile page with booking info and history."""
    guest = get_object_or_404(Guest, pk=guest_id)
    bookings = Booking.objects.filter(guest=guest).select_related('room').order_by('-created_at')
    latest_booking = bookings.first()
    context = {
        'guest': guest,
        'latest_booking': latest_booking,
        'bookings': bookings,
    }
    return render(request, 'hotel/guest_profile.html', context)


def rooms_list(request):
    """All rooms listing."""
    rooms = Room.objects.all()
    available = rooms.filter(is_available=True).count()
    occupied = rooms.filter(is_available=False).count()
    return render(request, 'hotel/rooms.html', {
        'rooms': rooms,
        'available_count': available,
        'occupied_count': occupied,
    })


def room_detail(request, room_id):
    """Room detail page."""
    room = get_object_or_404(Room, pk=room_id)
    bookings = Booking.objects.filter(room=room).select_related('guest').order_by('-created_at')
    context = {
        'room': room,
        'bookings': bookings,
    }
    return render(request, 'hotel/room_detail.html', context)


def financials(request):
    """Billing / financials view."""
    bookings = Booking.objects.select_related('guest', 'room').order_by('-created_at')
    total_revenue = sum(b.total_price for b in bookings if b.is_paid)
    paid_count = sum(1 for b in bookings if b.is_paid)
    unpaid_count = sum(1 for b in bookings if not b.is_paid)
    avg_value = round(total_revenue / paid_count, 2) if paid_count else 0
    context = {
        'bookings': bookings,
        'total_revenue': total_revenue,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'avg_value': avg_value,
    }
    return render(request, 'hotel/financials.html', context)


def reservations(request):
    """Full reservations list with filter."""
    status_filter = request.GET.get('status', 'All')
    bookings = Booking.objects.select_related('guest', 'room').order_by('-created_at')
    counts = {
        'All': bookings.count(),
        'Confirmed': bookings.filter(status='Confirmed').count(),
        'Checked_In': bookings.filter(status='Checked-In').count(),
        'Pending': bookings.filter(status='Pending').count(),
        'Checked_Out': bookings.filter(status='Checked-Out').count(),
        'Cancelled': bookings.filter(status='Cancelled').count(),
    }
    if status_filter != 'All':
        bookings = bookings.filter(status=status_filter)
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'counts': counts,
    }
    return render(request, 'hotel/reservations.html', context)


def messages_view(request):
    """Messages / communication view."""
    guests = Guest.objects.all()
    bookings = Booking.objects.select_related('guest', 'room').order_by('-created_at')
    return render(request, 'hotel/messages.html', {'guests': guests, 'bookings': bookings})


def housekeeping(request):
    """Housekeeping room status view."""
    rooms = Room.objects.all()
    return render(request, 'hotel/housekeeping.html', {'rooms': rooms})


def inventory(request):
    """Inventory management view."""
    return render(request, 'hotel/inventory.html', {})


def calendar_view(request):
    """Booking calendar view."""
    bookings = Booking.objects.select_related('guest', 'room').order_by('check_in')
    return render(request, 'hotel/calendar.html', {'bookings': bookings})


def reviews(request):
    """Guest reviews view."""
    guests = Guest.objects.all()
    return render(request, 'hotel/reviews.html', {'guests': guests})


def concierge(request):
    """Concierge / service requests view."""
    bookings = Booking.objects.select_related('guest', 'room').filter(
        status__in=['Confirmed', 'Checked-In']
    ).order_by('-created_at')
    return render(request, 'hotel/concierge.html', {'bookings': bookings})


def settings_view(request):
    """Hotel settings page."""
    return render(request, 'hotel/settings.html', {})


import uuid
import datetime

def book_room(request, room_id):
    """Book a new room."""
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        num_guests = request.POST.get('num_guests', 1)
        
        # Get or create Guest
        guest, created = Guest.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'guest_id': f"G-{uuid.uuid4().hex[:6].upper()}"
            }
        )
        if not created:
            guest.first_name = first_name
            guest.last_name = last_name
            guest.phone = phone
            guest.save()
            
        # Parse dates
        from django.utils.dateparse import parse_datetime
        # Use timezone aware datetimes if USE_TZ is true, but strptime is often fine for simple examples
        if 'T' not in check_in:
            check_in += 'T14:00:00'
        if 'T' not in check_out:
            check_out += 'T11:00:00'
            
        booking = Booking.objects.create(
            booking_id=f"BKG-{uuid.uuid4().hex[:6].upper()}",
            guest=guest,
            room=room,
            check_in=parse_datetime(check_in) or datetime.datetime.strptime(check_in[:10], '%Y-%m-%d'),
            check_out=parse_datetime(check_out) or datetime.datetime.strptime(check_out[:10], '%Y-%m-%d'),
            num_adults=int(num_guests),
            status='Confirmed'
        )
        return redirect('booking_confirmation', booking_id=booking.booking_id)

    return render(request, 'hotel/book_room.html', {'room': room})


def booking_confirmation(request, booking_id):
    """Show booking confirmation."""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, 'hotel/booking_confirmation.html', {'booking': booking})
