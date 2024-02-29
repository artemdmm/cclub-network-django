from django.contrib import admin

from .models import Room
from .models import Message

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)