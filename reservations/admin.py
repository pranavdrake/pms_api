from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
class CardDetailAdmin(SimpleHistoryAdmin):
    exclude = ['masked_card_number','masked_cvv_cvc']

admin.site.register(Property, SimpleHistoryAdmin)
admin.site.register(Block, SimpleHistoryAdmin)
admin.site.register(Floor, SimpleHistoryAdmin)
admin.site.register(RoomType, SimpleHistoryAdmin)
admin.site.register(Room, SimpleHistoryAdmin)
admin.site.register(RoomDiscrepancy, SimpleHistoryAdmin)
admin.site.register(Overbooking, SimpleHistoryAdmin)
admin.site.register(RoomTypeInventory, SimpleHistoryAdmin)
admin.site.register(ReasonGroup, SimpleHistoryAdmin)
admin.site.register(Reason, SimpleHistoryAdmin)
admin.site.register(Group, SimpleHistoryAdmin)
admin.site.register(SubGroup, SimpleHistoryAdmin)
admin.site.register(Extra, SimpleHistoryAdmin)
admin.site.register(Commission, SimpleHistoryAdmin)
admin.site.register(PickupDropDetails, SimpleHistoryAdmin)
admin.site.register(PreferenceGroup, SimpleHistoryAdmin)
admin.site.register(Preference, SimpleHistoryAdmin)
admin.site.register(MarketGroup, SimpleHistoryAdmin)
admin.site.register(MarketCode, SimpleHistoryAdmin)
admin.site.register(SourceGroup, SimpleHistoryAdmin)
admin.site.register(Source, SimpleHistoryAdmin)
admin.site.register(TransactionCode, SimpleHistoryAdmin)
admin.site.register(PackageGroup, SimpleHistoryAdmin)
admin.site.register(Package, SimpleHistoryAdmin)
admin.site.register(RateClass, SimpleHistoryAdmin)
admin.site.register(RateCategory, SimpleHistoryAdmin)
admin.site.register(RateCode, SimpleHistoryAdmin)
admin.site.register(RateCodeRoomRate, SimpleHistoryAdmin)
admin.site.register(PaymentType, SimpleHistoryAdmin)
admin.site.register(RoomMove, SimpleHistoryAdmin)
admin.site.register(AdjustTransaction, SimpleHistoryAdmin)
admin.site.register(TicketCategory, SimpleHistoryAdmin)
admin.site.register(Ticket, SimpleHistoryAdmin)
admin.site.register(SharingID, SimpleHistoryAdmin)
admin.site.register(ReservationType, SimpleHistoryAdmin)
admin.site.register(GroupReservation, SimpleHistoryAdmin)
admin.site.register(GroupReservationRoomType, SimpleHistoryAdmin)
admin.site.register(CardDetail, CardDetailAdmin)
admin.site.register(Reservation, SimpleHistoryAdmin)
admin.site.register(Folio, SimpleHistoryAdmin)
admin.site.register(Invoice, SimpleHistoryAdmin)
admin.site.register(Transaction, SimpleHistoryAdmin)
admin.site.register(RoomOccupancy, SimpleHistoryAdmin)
admin.site.register(WaitList, SimpleHistoryAdmin)
admin.site.register(DailyDetail, SimpleHistoryAdmin)
admin.site.register(DocumentType, SimpleHistoryAdmin)
admin.site.register(Document, SimpleHistoryAdmin)
admin.site.register(Alert, SimpleHistoryAdmin)
admin.site.register(RateSummary, SimpleHistoryAdmin)
admin.site.register(OutofOrderandService, SimpleHistoryAdmin)
admin.site.register(NightAudit, SimpleHistoryAdmin)
admin.site.register(Forex, SimpleHistoryAdmin)
admin.site.register(FixedCharge, SimpleHistoryAdmin)
admin.site.register(RoutingCode, SimpleHistoryAdmin)
admin.site.register(Routing, SimpleHistoryAdmin)
admin.site.register(Cancellation, SimpleHistoryAdmin)
admin.site.register(Reinstate, SimpleHistoryAdmin)

# from django.apps import apps

# # Get all models
# models = apps.get_models()

# for model in models:
#     # Register each model with Django Admin
#     admin.site.register(model)