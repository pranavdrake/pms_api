from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
import accounts.models 
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from datetime import *
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
    history = HistoricalRecords()
    def __str__(self):
        return self.commission_code

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
    history = HistoricalRecords()
    def __str__(self):
        return self.type + 'on' + str(self.date) + + 'at'+ str(self.time)

    class Meta:
        verbose_name  = 'Pickup / Drop Details'
        verbose_name_plural  = 'Pickup / Drop Details'

class PreferenceGroup(models.Model):
    preference_group = models.CharField(max_length=255, unique = True)
    description = models.TextField(blank = True, null  =True)
    history = HistoricalRecords()
    def __str__(self):
        return self.preference_group

class Preference(models.Model):
    preference_group = models.ForeignKey(PreferenceGroup, on_delete=models.CASCADE,related_name='preferences')
    preference = models.CharField(max_length=255)
    description = models.TextField(blank = True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.preference


class MarketGroup(models.Model):
    market_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.market_group

class MarketCode(models.Model):
    market_group = models.ForeignKey(MarketGroup, on_delete=models.CASCADE,related_name='market_codes')
    market_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.market_code

class SourceGroup(models.Model):
    source_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.source_group

class Source(models.Model):
    source_group = models.ForeignKey(SourceGroup, on_delete=models.CASCADE, related_name='sources')
    source_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.source_code



class TransactionCode(models.Model):
    transaction_code = models.CharField(max_length=255)
    description = models.TextField(blank = True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name= 'transaction_codes')
    sub_group = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name= 'transaction_codes')
    base_rate = models.DecimalField(max_digits=8, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    discount_allowed = models.BooleanField(default=False)
    is_allowance = models.BooleanField(default=False)
    allowance_code = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    commission_service_charge_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    history = HistoricalRecords()

    def __str__(self):
        return self.transaction_code

class PackageGroup(models.Model):
    package_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank= True, null= True)
    history = HistoricalRecords()

    def __str__(self):
        return self.package_group

class Package(models.Model):

    
    package_group = models.ForeignKey(PackageGroup, on_delete=models.CASCADE, related_name= 'packages')
    package_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank= True, null= True)
    begin_sell_date = models.DateField()
    end_sell_date = models.DateField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField()
    CALCULATION_RULE_CHOICES = (
    ('flat_rate', 'Flat Rate'),
    ('per_adult', 'Per Adult'),
    )
    calculation_rule = models.CharField(max_length=20, choices=CALCULATION_RULE_CHOICES)
    POSTING_RHYTHM_CHOICES = (
    ('post_every_night', 'Post Every Night'),
    ('post_on_arrival_night', 'Post on Arrival Night'),
    ('post_last_night', 'Post Last Night'),
    ('post_every_night_except_arrival_night', 'Post Every Night Except Arrival Night'),
    )
    posting_rhythm = models.CharField(max_length=50, choices=POSTING_RHYTHM_CHOICES)
    RATE_INCLUSION_CHOICES = (
    ('included_in_rate', 'Included in Rate'),
    ('add_rate_separate_line', 'Add Rate Separate Line'),
    )
    rate_inclusion = models.CharField(max_length=50, choices=RATE_INCLUSION_CHOICES)
    transaction_code = models.ForeignKey(TransactionCode, on_delete=models.CASCADE, related_name='packages')
    history = HistoricalRecords()

    def clean(self):
        if(self.begin_sell_date and self.end_sell_date):
            if self.begin_sell_date >  self.end_sell_date:
                raise ValidationError("Begin Sell Date cannot be more than end sell date")

        if self.percentage:   
            if self.percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")
            elif self.percentage < 0:
                raise ValidationError("Percentage cannot be negative")

        if self.base_price:
            if self.base_price < 0:
                raise ValidationError("Base Price cannot be negative")

        if(self.tax_percentage):
            if self.tax_percentage < 0:
                raise ValidationError("Tax Percentage cannot be negative")
            elif self.tax_percentage > 100:
                raise ValidationError("Tax Percentage cannot be more than 100")

    def save(self, *args, **kwargs):
        self.full_clean()
        self.tax_amount = (self.tax_percentage/100) * self.base_price 
        self.total_amount = self.base_price + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return self.package_code

class RateClass(models.Model):
    rate_class = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.rate_class

class RateCategory(models.Model):
    rate_class = models.ForeignKey(RateClass, on_delete=models.CASCADE,related_name='rate_categories')
    rate_category = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.rate_category

class RateCode(models.Model):
    rate_category = models.ForeignKey(RateCategory, on_delete=models.CASCADE,related_name='rate_codes')
    rate_code = models.CharField(max_length=200, unique = True)
    description = models.TextField(blank = True, null=True)
    market = models.ForeignKey(MarketCode,null=True, blank=True, on_delete=models.SET_NULL, related_name='rate_codes')
    source = models.ForeignKey(Source,null=True, blank=True, on_delete=models.SET_NULL, related_name='rate_codes')
    begin_sell_date = models.DateField()
    end_sell_date = models.DateField()
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name='rate_codes')
    extras = models.ManyToManyField(Extra, blank=True)
    transaction_code = models.ForeignKey(TransactionCode, on_delete=models.CASCADE, related_name='rate_codes')
    package_transaction_code = models.ForeignKey(TransactionCode, null=True, blank=True, on_delete=models.SET_NULL, related_name='package_rate_codes')
    room_types = models.ManyToManyField(RoomType)
    DAYS_APPLICABLE = [
    ('M', 'Monday'),
    ('T', 'Tuesday'),
    ('W', 'Wednesday'),
    ('TH', 'Thursday'),
    ('F', 'Friday'),
    ('SA', 'Saturday'),
    ('SU', 'Sunday')
    ]
    days_applicable = models.CharField(max_length=2, choices=DAYS_APPLICABLE, blank=True, null= True)
    print_rate = models.BooleanField(default = True)
    day_use = models.BooleanField(default = False)
    discount = models.BooleanField(default = False)
    discount_amount = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null= True)
    discount_percentage = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null= True )
    complimentary = models.BooleanField(default = False,blank=True, null= True)
    house_use = models.BooleanField(default = False,blank=True, null= True)
    history = HistoricalRecords()

    def clean(self):
        if(self.begin_sell_date and self.end_sell_date):
            if self.begin_sell_date >  self.end_sell_date:
                raise ValidationError("Begin Sell Date cannot be more than end sell date")

        if self.discount_amount:
            if self.discount_amount < 0:
                raise ValidationError("Discount Amount cannot be negative")

        if(self.discount_percentage):
            if self.discount_percentage < 0:
                raise ValidationError("Discount Percentage cannot be negative")
            elif self.discount_percentage > 100:
                raise ValidationError("Discount Percentage cannot be more than 100")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.rate_code

class RateCodeRoomRate(models.Model):
    rate_code = models.ForeignKey(RateCode, on_delete=models.CASCADE, related_name= 'rate_code_room_rates')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name= 'rate_code_room_rates')
    adult_price_1 = models.DecimalField(max_digits=5, decimal_places=2)
    adult_price_2 = models.DecimalField(max_digits=5, decimal_places=2)
    adult_price_3 = models.DecimalField(max_digits=5, decimal_places=2)
    extra_adult_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null= True)
    extra_child_price = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null= True)

    def clean(self):

        if self.adult_price_1 or self.adult_price_2 or self.adult_price_3 or self.extra_adult_price or self.extra_child_price:
            if self.adult_price_1 < 0 or self.adult_price_2 < 0 or self.adult_price_3 < 0  or self.extra_adult_price < 0 or self.extra_child_price < 0:
                raise ValidationError("Price cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return  'Room Rate for' + self.rate_code 


class PaymentType(models.Model):
    payment_type_code = models.CharField(max_length=255 ,unique=True)
    description = models.TextField(blank= True, null= True)
    transaction_code = models.ForeignKey(TransactionCode, on_delete=models.CASCADE, related_name='PaymentTypes') 
    history = HistoricalRecords()

    def __str__(self):
        return self.payment_type_code

class RoomMove(models.Model):
    from_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_moves_from')
    to_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_moves_to')
    reason_code = models.ForeignKey(Reason,on_delete=models.CASCADE, related_name='room_moves')
    reason_text = models.TextField(blank=True, null=True)
    history = HistoricalRecords()
    def clean(self):

            if self.from_room == self.to_room:
                raise ValidationError("From Room and Moved Room should be not same")

    def __str__(self):
        return self.from_room

class AdjustTransaction(models.Model):
    ADJUST_BY = [
    ('percentage', 'Percentage'),
    ('amount', 'Amount'),
    ]
    adjust_by = models.CharField(max_length=100, choices=ADJUST_BY, blank=False, null= False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reason = models.ForeignKey(Reason,on_delete=models.CASCADE, related_name='adjust_Transaction')
    reason_text = models.TextField(blank=True, null=True)
    reference = models.ForeignKey("accounts.CustomUser",on_delete=models.CASCADE, related_name='adjust_Transaction_user',default='')
    history = HistoricalRecords()
    
    
    def __str__(self):
        return self.adjust_by

class TicketCategory(models.Model):
    ticket_category_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.ticket_category_code 

class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]
    STATUS_CHOICES = [
        ('resolved', 'Resolved'),
        ('Unsolved', 'Unsolved')
    ] 
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='room_tickets')
    area = models.TextField(blank = True, null=True)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE,related_name='category_tickets')
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    Subject = models.CharField( max_length=255, blank = False, null=False)
    description = models.CharField(max_length=255, blank = True, null=True)
    # file_upload = models.FileField(_(""), upload_to=None, max_length=100)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    agent = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE,related_name='user_tickets')
    sla_date_and_time = models.DateTimeField()
    history = HistoricalRecords()

    def clean(self):
        today = datetime.datetime.now()
        if today > self.sla_date_and_time:
                raise ValidationError("SLA date time cannot be lesser then Current date time ")

    def save(self, *args, **kwargs):
        self.full_clean()

    def __str__(self):
        return  self.sla_date_and_time