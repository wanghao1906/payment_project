from django.contrib import admin
from .models import User, Bill

# Register your models here.

admin.site.register(User)
admin.site.register(Bill)