"""
Seed script – run with:
  python manage.py shell < seed_data.py
"""
import os, django, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import datetime, timedelta
from django.utils import timezone
from hotel.models import Room, Guest, Booking

# Clear existing data
print("Clearing old data…")
Booking.objects.all().delete()
Guest.objects.all().delete()
Room.objects.all().delete()

print("Seeding database with Indian data…")

# ── Rooms ──────────────────────────────────────────────────────────────────────
rooms_data = [
    dict(room_number="101", room_type="Standard",     price_per_night=4500,  size_sqm=25, bed_type="Double Bed",  max_guests=2, amenities="Free Wi-Fi, Room Service, Flat-screen TV, Air Conditioning", is_available=True),
    dict(room_number="102", room_type="Standard",     price_per_night=4800,  size_sqm=28, bed_type="Twin Beds",   max_guests=2, amenities="Free Wi-Fi, Room Service, Air Conditioning",                  is_available=True),
    dict(room_number="201", room_type="Deluxe",       price_per_night=8500,  size_sqm=35, bed_type="King Bed",    max_guests=2, amenities="Free Wi-Fi, Mini Bar, Room Service, Flat-screen TV, Bathtub", is_available=True),
    dict(room_number="202", room_type="Deluxe",       price_per_night=9200,  size_sqm=38, bed_type="King Bed",    max_guests=3, amenities="Free Wi-Fi, Mini Bar, Room Service, Balcony View",            is_available=False),
    dict(room_number="301", room_type="Suite",        price_per_night=18000, size_sqm=60, bed_type="King Bed",    max_guests=4, amenities="Free Wi-Fi, Mini Bar, Jacuzzi, Room Service, Balcony, Flat-screen TV, Private Lounge", is_available=True),
    dict(room_number="302", room_type="Suite",        price_per_night=22000, size_sqm=70, bed_type="King Bed",    max_guests=4, amenities="Free Wi-Fi, Mini Bar, Jacuzzi, Room Service, Balcony, Sea View",                       is_available=False),
    dict(room_number="305", room_type="Suite",        price_per_night=19500, size_sqm=65, bed_type="Queen Bed",   max_guests=3, amenities="Free Wi-Fi, Mini Bar, Room Service, Mountain View",           is_available=True),
    dict(room_number="401", room_type="Presidential", price_per_night=45000, size_sqm=150,bed_type="King Bed",    max_guests=6, amenities="Free Wi-Fi, Mini Bar, Jacuzzi, Gym Access, Butler Service, Balcony, Private Pool, Home Theatre", is_available=True),
]
rooms = {}
for d in rooms_data:
    r, _ = Room.objects.get_or_create(room_number=d["room_number"], defaults=d)
    rooms[d["room_number"]] = r
print(f"  {len(rooms)} rooms created.")

# ── Guests ─────────────────────────────────────────────────────────────────────
guests_data = [
    dict(guest_id="AH-G001", first_name="Arjun",    last_name="Sharma",   email="arjun.sharma@gmail.com",    phone="+91 98765 43210", date_of_birth="1985-06-15", gender="Male",   nationality="Indian", passport_number="P1234567",  loyalty_status="Platinum", loyalty_tier="Elite",    points_balance=15000),
    dict(guest_id="AH-G002", first_name="Priya",    last_name="Mehta",    email="priya.mehta@gmail.com",     phone="+91 99234 56780", date_of_birth="1990-03-22", gender="Female", nationality="Indian", passport_number="P7654321",  loyalty_status="Gold",     loyalty_tier="Gold",     points_balance=8200),
    dict(guest_id="AH-G003", first_name="Rahul",    last_name="Patel",    email="rahul.patel@outlook.com",   phone="+91 87654 32109", date_of_birth="1978-11-08", gender="Male",   nationality="Indian", passport_number="P1122334",  loyalty_status="Silver",   loyalty_tier="Silver",   points_balance=3400),
    dict(guest_id="AH-G004", first_name="Kavya",    last_name="Reddy",    email="kavya.reddy@gmail.com",     phone="+91 76543 21098", date_of_birth="1995-07-30", gender="Female", nationality="Indian", passport_number="P9988776",  loyalty_status="None",     loyalty_tier="",         points_balance=0),
    dict(guest_id="AH-G005", first_name="Vikram",   last_name="Singh",    email="vikram.singh@yahoo.com",    phone="+91 91234 56789", date_of_birth="1982-02-14", gender="Male",   nationality="Indian", passport_number="P5544332",  loyalty_status="Gold",     loyalty_tier="Gold",     points_balance=6800),
    dict(guest_id="AH-G006", first_name="Ananya",   last_name="Iyer",     email="ananya.iyer@gmail.com",     phone="+91 95678 12345", date_of_birth="1998-09-05", gender="Female", nationality="Indian", passport_number="P3322115",  loyalty_status="Silver",   loyalty_tier="Silver",   points_balance=2100),
    dict(guest_id="AH-G007", first_name="Rohit",    last_name="Gupta",    email="rohit.gupta@gmail.com",     phone="+91 93456 78901", date_of_birth="1975-12-19", gender="Male",   nationality="Indian", passport_number="P6677889",  loyalty_status="Platinum", loyalty_tier="Platinum", points_balance=22000),
    dict(guest_id="AH-G008", first_name="Meera",    last_name="Nair",     email="meera.nair@gmail.com",      phone="+91 97890 23456", date_of_birth="1993-04-11", gender="Female", nationality="Indian", passport_number="P8899001",  loyalty_status="None",     loyalty_tier="",         points_balance=500),
]
guests = {}
for d in guests_data:
    dob = datetime.strptime(d.pop("date_of_birth"), "%Y-%m-%d").date()
    g, _ = Guest.objects.get_or_create(guest_id=d["guest_id"], defaults={**d, "date_of_birth": dob})
    guests[d["guest_id"]] = g
print(f"  {len(guests)} guests created.")

# ── Bookings ───────────────────────────────────────────────────────────────────
def dt(date_str, time_str="14:00"):
    dt_naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    return timezone.make_aware(dt_naive)

bookings_data = [
    dict(
        booking_id="AH-B001",
        guest_id="AH-G001", room_number="201",
        check_in=dt("2025-07-10", "14:00"), check_out=dt("2025-07-13", "11:00"),
        num_adults=2, num_children=0,
        special_requests="Non-smoking room, extra pillows. Airport pickup needed.",
        status="Confirmed",
        complimentary_breakfast=True, free_wifi=True, gym_pool_access=True,
        transportation="Airport pickup arranged",
        extras_amount=0, vat_percent=12, city_tax=800,
        billing_notes="Corporate billing – Infosys Ltd. Payment confirmed.",
        is_paid=True,
    ),
    dict(
        booking_id="AH-B002",
        guest_id="AH-G001", room_number="301",
        check_in=dt("2025-04-01", "15:00"), check_out=dt("2025-04-05", "11:00"),
        num_adults=2, num_children=1,
        special_requests="Early check-in requested. Child menu needed.",
        status="Checked-Out",
        complimentary_breakfast=True, free_wifi=True, gym_pool_access=False,
        transportation="",
        extras_amount=2500, vat_percent=12, city_tax=800,
        billing_notes="",
        is_paid=True,
    ),
    dict(
        booking_id="AH-B003",
        guest_id="AH-G002", room_number="302",
        check_in=dt("2025-07-20", "14:00"), check_out=dt("2025-07-24", "12:00"),
        num_adults=2, num_children=0,
        special_requests="Sea-view balcony preferred. Vegan meal options.",
        status="Confirmed",
        complimentary_breakfast=True, free_wifi=True, gym_pool_access=True,
        transportation="Car hire arranged",
        extras_amount=0, vat_percent=12, city_tax=800,
        billing_notes="",
        is_paid=False,
    ),
    dict(
        booking_id="AH-B004",
        guest_id="AH-G003", room_number="101",
        check_in=dt("2025-08-05", "14:00"), check_out=dt("2025-08-08", "11:00"),
        num_adults=1, num_children=0,
        special_requests="",
        status="Pending",
        complimentary_breakfast=False, free_wifi=True, gym_pool_access=False,
        transportation="",
        extras_amount=0, vat_percent=12, city_tax=500,
        billing_notes="",
        is_paid=False,
    ),
    dict(
        booking_id="AH-B005",
        guest_id="AH-G004", room_number="401",
        check_in=dt("2025-09-10", "16:00"), check_out=dt("2025-09-15", "12:00"),
        num_adults=3, num_children=1,
        special_requests="Champagne, flowers, and rose petals on arrival. Honeymoon decoration.",
        status="Confirmed",
        complimentary_breakfast=True, free_wifi=True, gym_pool_access=True,
        transportation="Limousine service from Mumbai Airport",
        extras_amount=8000, vat_percent=12, city_tax=800,
        billing_notes="VIP package applied. Tata Group corporate booking.",
        is_paid=True,
    ),
    dict(
        booking_id="AH-B006",
        guest_id="AH-G005", room_number="202",
        check_in=dt("2025-07-15", "14:00"), check_out=dt("2025-07-17", "11:00"),
        num_adults=2, num_children=0,
        special_requests="Late check-out if possible.",
        status="Checked-In",
        complimentary_breakfast=True, free_wifi=True, gym_pool_access=True,
        transportation="",
        extras_amount=1500, vat_percent=12, city_tax=800,
        billing_notes="",
        is_paid=False,
    ),
    dict(
        booking_id="AH-B007",
        guest_id="AH-G006", room_number="102",
        check_in=dt("2025-06-20", "13:00"), check_out=dt("2025-06-22", "11:00"),
        num_adults=1, num_children=0,
        special_requests="Quiet room away from elevator.",
        status="Checked-Out",
        complimentary_breakfast=False, free_wifi=True, gym_pool_access=False,
        transportation="",
        extras_amount=0, vat_percent=12, city_tax=500,
        billing_notes="",
        is_paid=True,
    ),
    dict(
        booking_id="AH-B008",
        guest_id="AH-G007", room_number="305",
        check_in=dt("2025-08-25", "15:00"), check_out=dt("2025-08-30", "11:00"),
        num_adults=2, num_children=2,
        special_requests="Baby cot and high chair needed. Nut-free meals for children.",
        status="Confirmed",
        complimentary_breakfast=True, free_wifi=True, gym_pool_access=True,
        transportation="Cab from Pune Railway Station",
        extras_amount=3000, vat_percent=12, city_tax=800,
        billing_notes="Loyalty discount applied – 10%.",
        is_paid=True,
    ),
]

for d in bookings_data:
    g = guests[d.pop("guest_id")]
    r = rooms[d.pop("room_number")]
    Booking.objects.get_or_create(booking_id=d["booking_id"], defaults={**d, "guest": g, "room": r})

print(f"  {len(bookings_data)} bookings created.")
print("✅  Seed complete with Indian data! Visit http://127.0.0.1:8000 to explore.")
print("   Admin: http://127.0.0.1:8000/admin/")
