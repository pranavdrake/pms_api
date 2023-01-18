
from django.urls import path
from .views import *

urlpatterns = [
    path('import-accounts/', import_accounts),
    path('import-bookers/', import_bookers),
    path('import-guests/', import_guests),
]