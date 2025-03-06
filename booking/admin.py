# Register your models here.
from django.contrib import admin
from .models import Table, Reservation


class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'location')
    search_fields = ('number', 'location')
    list_filter = ('capacity', 'location')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'date', 'time', 'party_size')
    search_fields = ('user__username', 'table__number', 'date')
    list_filter = ('date', 'time', 'party_size')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')


admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
