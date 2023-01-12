from django.urls import path
from .views import *

urlpatterns = [
   path('import-bookers/', import_bookers),
]