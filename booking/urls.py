from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking-options/', views.booking_options, name='booking_options'),
    path('book-table/', views.book_table, name='book_table'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
]