from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Table {self.number} - {self.capacity} seats"


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()

    def __str__(self):
        return f"Reservation for {self.table} on {self.date} at {self.time}"
