from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Property(models.Model):
    property_name = models.CharField(max_length=250)
    country = CountryField()
    currency = models.CharField(max_length=3)
    address = models.TextField()

    def __str__(self):
        return  self.property

    class Meta:
        verbose_name_plural  = 'Properties'

class Block(models.Model):
    property  = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'blocks')
    block = models.CharField(max_length=250)

    def __str__(self):
        return self.block +' ' + self.property

class Floor(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'floors')
    block = models.ForeignKey(Block, blank = True, null = True, on_delete=models.SET_NULL)
    floor = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.floor +' ' + self.property

class RoomType(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'room_types')
    room_type = models.CharField(max_length=100)
    max_adults = models.PositiveSmallIntegerField()
    max_children = models.PositiveSmallIntegerField()
    total_number_of_rooms = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.room_type + ' ' + self.property

class Room(models.Model):

    ROOM_STATUS_CHOICES = [
        ('clean', 'Clean'),
        ('inspected', 'Inspected'),
        ('dirty', 'Dirty'),
        ('out_of_order', 'Out of Order'),
        ('out_of_service', 'Out of Service')
    ]

    FRONT_OFFICE_STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied')
    ]

    RESERVATION_STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('departed', 'Departed'),
        ('stay_over', 'Stay Over'),
        ('arrivals', 'Arrivals'),
        ('not_reserved', 'Not Reserved'),
        ('arrived', 'Arrived'),
        ('due_out', 'Due Out'),
        ('due_out_arrivals', 'Due Out / Arrivals')
    ]

    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name= 'rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE,related_name= 'rooms')
    room_number = models.PositiveSmallIntegerField()
    room_status = models.CharField(max_length=100, choices=ROOM_STATUS_CHOICES)
    front_office_status = models.CharField(max_length=100, choices=FRONT_OFFICE_STATUS_CHOICES)
    reservation_status = models.CharField(max_length=100, choices=RESERVATION_STATUS_CHOICES)

    def __str__(self):
        return self.room_number + ' ' + self.property 

