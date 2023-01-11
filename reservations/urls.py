from django.urls import path
from .views import *


urlpatterns = [
    path('import-market-groups/', import_market_groups),
    path('import-market-codes/', import_market_codes),
    path('import-room-types/', import_room_types),
    path('import-rooms/', import_rooms),
    path('import-source-groups/',import_source_groups),   
    path('import-extra/',import_extra),
    path('import-package-group/',import_package_group),
    path('import-package/',import_package),
]