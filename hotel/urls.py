from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('guest/<int:guest_id>/', views.guest_profile, name='guest_profile'),
    path('rooms/', views.rooms_list, name='rooms_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('booking/<str:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('financials/', views.financials, name='financials'),
    path('reservations/', views.reservations, name='reservations'),
    path('messages/', views.messages_view, name='messages'),
    path('housekeeping/', views.housekeeping, name='housekeeping'),
    path('inventory/', views.inventory, name='inventory'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('reviews/', views.reviews, name='reviews'),
    path('concierge/', views.concierge, name='concierge'),
    path('settings/', views.settings_view, name='settings'),
]
