from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Timing)
admin.site.register(Route)
admin.site.register(Booking)