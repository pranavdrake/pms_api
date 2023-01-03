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
admin.site.register(Commission)
admin.site.register(PickupDropDetails)
admin.site.register(PreferenceGroup)
admin.site.register(Preference)
admin.site.register(MarketGroup)
admin.site.register(MarketCode)
admin.site.register(SourceGroup)
admin.site.register(Source)
admin.site.register(TransactionCode)
admin.site.register(PackageGroup)
admin.site.register(Package)
admin.site.register(RateClass)
admin.site.register(RateCategory)
admin.site.register(RateCode)
admin.site.register(RateCodeRoomRate)