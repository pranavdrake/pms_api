from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField

# Create your models here.
class Property(models.Model):
    property_name = models.CharField(max_length=250)
    country = CountryField()
    currency = models.CharField(max_length=3)
    address = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return  self.property_name

    class Meta:
        verbose_name_plural  = 'Properties'

class Block(models.Model):
    property  = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'blocks')
    block = models.CharField(max_length=250)
    history = HistoricalRecords()
    def __str__(self):
        return self.block +' ' + self.property.property_name

class Floor(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'floors')
    block = models.ForeignKey(Block, blank = True, null = True, on_delete=models.SET_NULL)
    floor = models.PositiveSmallIntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.floor) +' ' + self.property.property_name

class RoomType(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'room_types')
    room_type = models.CharField(max_length=100)
    max_adults = models.PositiveSmallIntegerField()
    max_children = models.PositiveSmallIntegerField()
    total_number_of_rooms = models.PositiveSmallIntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return self.room_type + ' ' + self.property.property_name

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
    history = HistoricalRecords()

    def __str__(self):
        return str(self.room_number) + ' ' + self.property.property_name

class RoomDiscrepancy(models.Model):
    FRONT_OFFICE_STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied')
    ]
    HOUSEKEEPING_STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied')
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name= 'room_discrepancies')
    front_office_status = models.CharField(max_length=100, choices=FRONT_OFFICE_STATUS_CHOICES)
    housekeeping_status = models.CharField(max_length=100, choices=HOUSEKEEPING_STATUS_CHOICES)
    front_office_pax = models.PositiveSmallIntegerField()
    housekeeping_pax = models.PositiveSmallIntegerField()
    discrepancy = models.PositiveSmallIntegerField(default=0)
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        self.discrepancy = self.front_office_pax - self.housekeeping_pax
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Discrepancy for room {self.room} of {self.room.room_type.property}'

    class Meta:
        verbose_name_plural = 'Room Discrepancies'

class Overbooking(models.Model):

    overbooking_limit = models.PositiveSmallIntegerField()
    history = HistoricalRecords()
    
    def __str__(self):
        return f'Overbooking limit: {self.overbooking_limit}'

def validate_max_number_of_overbooked_rooms(value):
    if value > Overbooking.objects.first().overbooking_limit:
        raise ValidationError('Number of overbooked rooms cannot be greated than Overbooking Limit')

class RoomTypeInventory(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name= 'inventory')
    number_of_available_rooms = models.PositiveSmallIntegerField()
    number_of_overbooked_rooms = models.PositiveSmallIntegerField(validators=[validate_max_number_of_overbooked_rooms])
    date = models.DateField()
    history = HistoricalRecords()
    
    def clean(self):
        if self.number_of_available_rooms > self.room_type.total_number_of_rooms:
            raise ValidationError("Number of available rooms cannot be greater than Total number of rooms for this Room Type")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Inventory for {self.room_type} on {self.date}'
    class Meta:
        verbose_name_plural = 'Room Type Inventory'

class ReasonGroup(models.Model):
    reason_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True )
    history = HistoricalRecords()

    def __str__(self):
        return self.reason_group

class Reason(models.Model):
    reason_group = models.ForeignKey(ReasonGroup, on_delete=models.CASCADE, related_name= 'reasons')
    reason_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True)
    history = HistoricalRecords()

    def __str__(self):
        return self.reason_code

class Group(models.Model):
    group_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True)
    history = HistoricalRecords()

    def __str__(self):
        return self.group_code

class SubGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name= 'sub_groups')
    sub_group_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True)
    history = HistoricalRecords()

    def __str__(self):
        return self.sub_group_code
        
    class  Meta:
        verbose_name = 'Sub Group/ Outlet'
        verbose_name_plural = 'Sub Groups/ Outlets'

class Extra(models.Model):

    TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
        ('pieces', 'Pieces'),
        ('trips', 'Trips'),
    ]

    extra_code = models.CharField(max_length=255)
    description = models.TextField(blank= True, null= True)
    group = models.ManyToManyField(Group)
    sub_group = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pieces = models.IntegerField(null=True, blank=True)
    trips = models.IntegerField(null=True, blank=True)
    history = HistoricalRecords()

    def clean(self):
        if(self.percentage):
            if self.percentage < 0:
                raise ValidationError("Percentage cannot be negative")
            elif self.percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")

        elif self.amount:
            print(self.amount)
            if self.amount < 0:
                raise ValidationError("Amount cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.extra_code

class Commission(models.Model):
    commission_code = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank = True, null  =True)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.commission_code
        

class PreferenceGroup(models.Model):
    preference_group = models.CharField(max_length=255, unique = True)
    description = models.TextField(blank = True, null  =True)

    def __str__(self):
        return self.preference_group

class Preference(models.Model):
    preference_group = models.ForeignKey(PreferenceGroup, on_delete=models.CASCADE,related_name='preferences')
    preference = models.CharField(max_length=255)
    description = models.TextField(blank = True, null=True)

    def __str__(self):
        return self.preference

class RateClass(models.Model):
    rate_class = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.rate_class


class RateCategory(models.Model):
    rate_class = models.ForeignKey(RateClass, on_delete=models.CASCADE,related_name='rate_categories')
    rate_category = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.rate_category

class MarketGroup(models.Model):
    market_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)

    def __str__(self):
        return self.market_group

class MarketCode(models.Model):
    market_group = models.ForeignKey(MarketGroup, on_delete=models.CASCADE,related_name='market_codes')
    market_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.market_code

class SourceGroup(models.Model):
    source_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.source_group

class Source(models.Model):
    source_group = models.ForeignKey(SourceGroup, on_delete=models.CASCADE, related_name='sources')
    source_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.source_code

class PickupDropDetails(models.Model):
    TYPE_CHOICES = [
        ('pickup', 'Pickup'),
        ('drop', 'Drop'),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    station_code = models.CharField(max_length=255)
    carrier_code = models.CharField(max_length=255)
    transport_type = models.CharField(max_length=255)
    remarks = models.TextField(blank = True, null=True)

    def __str__(self):
        return self.type + 'on' + str(self.date) + + 'at'+ str(self.time)

    class Meta:
        verbose_name  = 'Pickup / Drop Details'
        verbose_name_plural  = 'Pickup / Drop Details'