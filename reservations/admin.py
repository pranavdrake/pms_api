from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Property)
admin.site.register(Block)
admin.site.register(Floor)
admin.site.register(RoomType)
admin.site.register(Room)