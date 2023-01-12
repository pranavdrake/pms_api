from django.urls import path
from .views import *

urlpatterns = [
    path('import-market-groups/', import_market_groups),
    path('import-market-codes/', import_market_codes),
    path('import-room-types/', import_room_types),
    path('import-rooms/', import_rooms),
    path('import-groups/', import_groups),
    path('import-sub-groups/', import_sub_groups),
    path('import-source-groups/',import_source_groups),   
    path('import-source-codes/', import_source_codes),
    path('import-rate-classes/', import_rate_classes),
    path('import-rate-categories/', import_rate_categories),
    path('import-forexes/', import_forexes),
    path('import-transaction-codes/', import_transaction_codes),
    path('import-extra/',import_extra),
    path('import-package-group/',import_package_group),
    path('import-package/',import_package),
    path('import-rate-codes/', import_rate_codes),
]