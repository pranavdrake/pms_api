from django.urls import path
from .views import *

urlpatterns = [
    path('import-accounts/', import_accounts),
    path('import-all-guests/', import_guest_profiles),

]