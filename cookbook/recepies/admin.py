from django.contrib import admin
from .models import Recepie, Quantity

# Register your models here.
admin.site.register(Recepie)
admin.site.register(Quantity)