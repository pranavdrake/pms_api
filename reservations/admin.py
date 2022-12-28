from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

admin.site.register(Property, SimpleHistoryAdmin)
admin.site.register(Block)
admin.site.register(Floor)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(RoomDiscrepancy)
admin.site.register(Overbooking)
admin.site.register(RoomTypeInventory)
admin.site.register(ReasonGroup)
admin.site.register(Reason)
admin.site.register(Group)
admin.site.register(SubGroup)
admin.site.register(Extra)