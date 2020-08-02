from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("bookPage", views.bookPage , name= "bookPage"),
    path("login", views.login_view, name="login"),
    path("register",views.register_view, name="register"),
    path("routes/<str:_from>/<str:to>", views.routes , name = "routes"),
    path("booking", views.booking, name="booking"),
    path("logout", views.logout_view, name="logout"),
    path("myBookings", views.myBookings, name= "myBookings"),
    path("history" , views.history , name="history")
]