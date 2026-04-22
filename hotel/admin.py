from django.contrib import admin
from .models import Room, Guest, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'bed_type', 'max_guests', 'is_available')
    list_filter = ('room_type', 'is_available', 'bed_type')
    search_fields = ('room_number',)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('guest_id', 'full_name', 'email', 'phone', 'loyalty_status', 'points_balance')
    list_filter = ('loyalty_status', 'gender', 'nationality')
    search_fields = ('guest_id', 'first_name', 'last_name', 'email')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'guest', 'room', 'check_in', 'check_out', 'status', 'is_paid')
    list_filter = ('status', 'is_paid', 'room__room_type')
    search_fields = ('booking_id', 'guest__first_name', 'guest__last_name')
    date_hierarchy = 'check_in'
