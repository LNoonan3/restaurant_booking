from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'party_size']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if table and date and time:
            if Reservation.objects.filter(table=table, date=date, time=time).exists():
                raise ValidationError('This table is already booked for the selected date and time.')

        return cleaned_data
