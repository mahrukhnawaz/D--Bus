from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    pass


class Route(models.Model):
    _from = models.CharField(max_length=100)
    to = models.CharField(max_length=100)
    price = models.FloatField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "from": self._from,
            "to": self.to,
            "price": self.price,
            "total_seats": self.total_seats
        }

class Timing(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure = models.TimeField()
    arival  = models.TimeField()
    total_seats = models.IntegerField(default=75)

    def serialize(self):
        return {
            "id": self.id,
            "price":  self.route.price,
            "total_seats": self.total_seats,
            "departure": self.departure.strftime("%I:%M %p"),
            "arival": self.arival.strftime("%I:%M %p")
        }
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    route = models.ForeignKey(Route,on_delete=models.CASCADE)
    timing = models.ForeignKey(Timing,on_delete=models.CASCADE)
    date = models.DateField()
    seats = models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            "price":  self.route.price,
            "from":  self.route._from,
            "to":  self.route.to,
            "departure": self.timing.departure.strftime("%I:%M %p"),
            "arival": self.timing.arival.strftime("%I:%M %p"),
            "date": self.date,
            "seats": self.seats
        }