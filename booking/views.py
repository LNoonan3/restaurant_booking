from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
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
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservation updated successfully.')
            return redirect('manage_reservations')
        else:
            messages.error(request, 'There was an error updating the reservation. Please try again.')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})


@login_required
@user_passes_test(is_admin)
def manage_reservations(request):
    reservations = Reservation.objects.all()

    user_filter = request.GET.get('user')
    date_filter = request.GET.get('date')
    table_filter = request.GET.get('table')

    if user_filter:
        reservations = reservations.filter(user__username__icontains=user_filter)
    if date_filter:
        reservations = reservations.filter(date=date_filter)
    if table_filter:
        reservations = reservations.filter(table__number=table_filter)

    return render(request, 'manage_reservations.html', {'reservations': reservations})


@login_required
def book_table(request):
    table_id = request.GET.get('table')
    if table_id:
        table = get_object_or_404(Table, id=table_id)
    else:
        table = None

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
        form = ReservationForm(initial={'table': table})

    return render(request, 'book_table.html', {'form': form, 'table': table})


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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email (you need to configure email settings in settings.py)
        send_mail(
            f'Message from {name}',
            message,
            email,
            ['info@restaurant.com'],
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')
