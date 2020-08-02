import json
import requests
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date

from .models import User,Route, Timing, Booking

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request,"Bus/welcome.html")

def bookPage(request):
    if request.method == "GET":
        return render(request, "Bus/index.html")


#login from for users
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Bus/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Bus/login.html")

#logout for users
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#registration for users
def register_view(request):
    if request.method == "POST":
        print("Hey in Register POST!")
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Bus/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Bus/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Bus/register.html")


#display timing of selected route and check if routes are valid
def routes(request ,_from, to):
    route = Route.objects.get(_from  = _from , to = to)
    timings = Timing.objects.filter(route = route)
    return JsonResponse([time.serialize() for time in timings], safe=False)

#request for booking
@csrf_exempt
def booking(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        _from = data.get("_from", "")
        to = data.get("to", "")
        date = data.get("date", "")
        _id = int(data.get("_id", ""))
        print(f"{_id}: is id")
        seats = data.get("seats", "")
        route = Route.objects.get(_from = _from,to=to)
        timing = Timing.objects.get(route = route,pk = _id)
        book = Booking(user=request.user,route=route,timing = timing,date=date,seats=seats)
        book.save()
        timing.total_seats -= int(seats)
        timing.save()

        return JsonResponse({"message": "Your Ticket is booked.", "status": 200}, status=200)
    return JsonResponse({"error": "Login Required.", "status": 300}, status=300)


#users Requested to how their bookings
def myBookings(request):
    booking = Booking.objects.filter(user = request.user)
    today = date.today()
    data = []
    for book in booking:
        data.append(book.serialize())
    return render(request,"Bus/bookings.html",{"data": data,"today":today})


#user want to check prevoius bookings
def history(request):
    booking = Booking.objects.filter(user = request.user)
    today = date.today()
    data = []
    for book in booking:
        data.append(book.serialize())
    return render(request,"Bus/history.html",{"data":data, "today": today})