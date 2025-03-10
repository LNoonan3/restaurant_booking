from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Table, Reservation
from .forms import ReservationForm
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'home.html')


def booking_options(request):
    tables = Table.objects.all()
    return render(request, 'booking_options.html', {'tables': tables})


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def manage_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'manage_reservations.html', {'reservations': reservations})


@login_required
def book_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, 'Your reservation has been confirmed!')
            return redirect('booking_confirmation')
        else:
            messages.error(request, 'There was an error with your booking. Please try again.')
    else:
        form = ReservationForm()
    return render(request, 'book_table.html', {'form': form})


@login_required
def my_bookings(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'reservations': reservations})


@login_required
def cancel_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    if reservation.user == request.user:
        reservation.delete()
        return redirect('my_bookings')
    return redirect('home')


def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def menu(request):
    return render(request, 'menu.html')


def contact(request):
    return render(request, 'contact.html')
