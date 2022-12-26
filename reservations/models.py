from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Property(models.Model):
    property_name = models.CharField(max_length=250)
    country = CountryField()
    currency = models.CharField(max_length=3)
    address = models.TextField()

