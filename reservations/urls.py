from django.urls import path
from .views import *

urlpatterns = [
    path('import-market-groups/', import_market_groups),
    path('import-market-codes/', import_market_codes),
    path('import-room-types/', import_room_types),
    path('import-rooms/', import_rooms),
    path('import-groups/', import_groups),
    path('import-sub-groups/', import_sub_groups),



]