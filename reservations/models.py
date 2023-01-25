from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
import accounts.models 
from simple_history.models import HistoricalRecords
from djmoney.models.fields import MoneyField
from datetime import *
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
import pycountry
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField
# Create your models here.
class Property(models.Model):
    CURRENCY_CHOICES =[(currency.alpha_3, f"{currency.name} ({currency.alpha_3})") for currency in pycountry.currencies]

    property_name = models.CharField(max_length=250)
    property_code = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField()
    currency = models.CharField(max_length=3,choices= CURRENCY_CHOICES)
    address = models.TextField()
    email = models.EmailField(max_length=250,blank = True, null = True)
    phone_number = models.CharField(max_length=20,blank = True, null = True)
    reservation_phone_number = models.CharField(max_length=20,blank = True, null = True)
    fax = models.CharField(max_length=20,blank = True, null = True)
    logo = models.FileField(upload_to='logos/',blank = True, null = True)
    property_type = models.CharField(max_length=20,blank = True, null = True)
    website = models.URLField(blank = True, null = True)
    registration_number = models.CharField(max_length=20,blank = True, null = True)
    business_date = models.DateField(null=True)
    financial_year = models.CharField(max_length=4,blank = True, null = True)
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

class PreferenceGroup(models.Model):
    preference_group = models.CharField(max_length=255, unique = True)
    description = models.TextField(blank = True, null  =True)
    is_active  = models.BooleanField(default = True)
    history = HistoricalRecords()
    def __str__(self):
        return self.preference_group  

class Preference(models.Model):
    preference_group = models.ForeignKey(PreferenceGroup, on_delete=models.CASCADE,related_name='preferences')
    preference = models.CharField(max_length=255)
    description = models.TextField(blank = True, null=True)
    is_active  = models.BooleanField(default = True)
    history = HistoricalRecords()
    def __str__(self):
        return self.preference

class RoomClass(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'room_classes')
    room_class = models.CharField(max_length=100)
    is_active  = models.BooleanField(default = True)
    history = HistoricalRecords()

class RoomType(models.Model):
    property = models.ForeignKey(Property,on_delete=models.CASCADE, related_name= 'room_types')
    room_class = models.ForeignKey(RoomClass,on_delete=models.CASCADE,null=True,blank=True, related_name= 'room_types')
    room_type = models.CharField(max_length=100)
    max_adults = models.PositiveSmallIntegerField()
    max_children = models.PositiveSmallIntegerField()
    total_number_of_rooms = models.PositiveSmallIntegerField()
    is_active  = models.BooleanField(default = True)
    history = HistoricalRecords()

    def __str__(self):
        return self.room_type + ' ' + self.property.property_name

class RoomImage(models.Model):
    file = models.FileField(upload_to='files/')
    history = HistoricalRecords()

class Room(models.Model):

    ROOM_STATUS_CHOICES = [
        ('Clean', 'Clean'),
        ('Inspected', 'Inspected'),
        ('Dirty', 'Dirty'),
        ('Out Of Order', 'Out Of Order'),
        ('Out Of Service', 'Out Of Service')
    ]

    FRONT_OFFICE_STATUS_CHOICES = [
        ('Vacant', 'Vacant'),
        ('Occupied', 'Occupied')
    ]

    RESERVATION_STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Departed', 'Departed'),
        ('Stay Over', 'Stay Over'),
        ('Arrivals', 'Arrivals'),
        ('Not Reserved', 'Not Reserved'),
        ('Arrived', 'Arrived'),
        ('Due Out', 'Due Out'),
        ('Due Out / Arrivals', 'Due Out / Arrivals')
    ]

    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name= 'rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE,related_name= 'rooms')
    room_number = models.PositiveSmallIntegerField()
    room_status = models.CharField(max_length=100, choices=ROOM_STATUS_CHOICES,default='Dirty')
    front_office_status = models.CharField(max_length=100, choices=FRONT_OFFICE_STATUS_CHOICES,default='Vacant')
    reservation_status = models.CharField(max_length=100, choices=RESERVATION_STATUS_CHOICES, default= 'Not Reserved')
    images = models.ManyToManyField(RoomImage,blank = True)
    features  = models.ManyToManyField(Preference,blank = True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.room_number) + ' ' + self.room_type.property.property_name

class RoomDiscrepancy(models.Model):
    FRONT_OFFICE_STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied')
    ]
    HOUSEKEEPING_STATUS_CHOICES = [
        ('Clean', 'Clean'),
        ('Inspected', 'Inspected'),
        ('Dirty', 'Dirty'),
        ('Out Of Order', 'Out Of Order'),
        ('Out Of Service', 'Out Of Service')
    ]
    RESERVATION_STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Departed', 'Departed'),
        ('Stay Over', 'Stay Over'),
        ('Arrivals', 'Arrivals'),
        ('Not Reserved', 'Not Reserved'),
        ('Arrived', 'Arrived'),
        ('Due Out', 'Due Out'),
        ('Due Out / Arrivals', 'Due Out / Arrivals')
    ]


    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name= 'room_discrepancies')
    housekeeping_status = models.CharField(max_length=100, choices=HOUSEKEEPING_STATUS_CHOICES, default='Dirty')
    front_office_status = models.CharField(max_length=100, choices=FRONT_OFFICE_STATUS_CHOICES,default='Vacant')
    reservation_status = models.CharField(max_length=100, choices=RESERVATION_STATUS_CHOICES, default= 'Not Reserved')
    front_office_pax = models.PositiveSmallIntegerField()
    housekeeping_pax = models.PositiveSmallIntegerField()
    discrepancy = models.PositiveSmallIntegerField(default=0)
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        if self.front_office_pax > self.housekeeping_pax:
            self.discrepancy = self.front_office_pax - self.housekeeping_pax
        else:
            self.discrepancy = self.housekeeping_pax - self.front_office_pax 

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
    number_of_sell_control_rooms = models.PositiveSmallIntegerField(blank = True, null=True)
    number_of_ood_rooms = models.PositiveSmallIntegerField(blank = True, null=True)
    number_of_overbooked_rooms = models.PositiveSmallIntegerField(validators=[validate_max_number_of_overbooked_rooms])
    sell_limit = models.PositiveSmallIntegerField(blank = True, null=True)
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
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.reason_group

class Reason(models.Model):
    reason_group = models.ForeignKey(ReasonGroup, on_delete=models.CASCADE, related_name= 'reasons')
    reason_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.reason_code

class Group(models.Model):
    group_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True)
    cost_center = models.CharField(max_length=255, blank = True, null = True)
    is_active  = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.group_code

class SubGroup(models.Model):
    group = models.ForeignKey(Group,blank = True, null = True, on_delete=models.CASCADE, related_name= 'sub_groups')
    sub_group_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null = True)
    is_active  = models.BooleanField(default=True)
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
    remarks = models.TextField(blank= True, null= True)
    group = models.ManyToManyField(Group, blank=True)
    sub_group = models.ForeignKey(SubGroup,blank= True, null= True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=255,null=True,blank=True, choices=TYPE_CHOICES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pieces = models.IntegerField(null=True, blank=True)
    trips = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def clean(self):
        if(self.percentage):
            if self.percentage < 0:
                raise ValidationError("Percentage cannot be negative")
            elif self.percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")

        elif self.amount:
            if self.amount < 0:
                raise ValidationError("Amount cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.extra_code

class PickupDropDetails(models.Model):
    TYPE_CHOICES = [
        ('pickup', 'Pickup'),
        ('drop', 'Drop'),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    date = models.DateField(null= True, blank= True)
    time = models.TimeField(null= True, blank= True)
    station_code = models.CharField(max_length=255, null= True, blank= True)
    carrier_code = models.CharField(max_length=255, null= True, blank= True)
    transport_type = models.CharField(max_length=255, null= True, blank= True)
    remarks = models.TextField(blank = True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.type + 'on' + str(self.date) + 'at'+ str(self.time)

    class Meta:
        verbose_name  = 'Pickup / Drop Details'
        verbose_name_plural  = 'Pickup / Drop Details'



class MarketGroup(models.Model):
    market_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
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

class Tax(models.Model):
    POSTING_TYPE_CHOICES = [
        ('slab', 'Slab'),
        ('flat amount','Flat Amount'),
        ('flat percentage','Flat Percentage'),

    ]

    APPLY_ON_PAX_CHOICES = [
        ('Per Night', 'Per Night'),
        ('Per Adult', 'Per Adult'),
        ('Per Child', 'Per Child'),
        ('Per Pax', 'Per Pax'),
    ]

    APPLY_TAX_CHOICES = [
        ('before discount', 'Before Discount'),
        ('after discount','After Discount'),

    ]
    
    tax_name = models.CharField(max_length=255, unique= True)
    applies_form = models.DateField()
    exempt_after = models.IntegerField(default = 0)
    posting_type = models.CharField(max_length=100, choices=POSTING_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    apply_on_pax  = models.CharField(max_length=100, choices=APPLY_ON_PAX_CHOICES,null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    no_of_slabs = models.IntegerField( null=True, blank=True)
    apply_tax = models.CharField(max_length=100, choices=APPLY_TAX_CHOICES,default= 'before discount')
    apply_tax_on_rack_rate = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def clean(self):
        if(self.tax_percentage):
            if self.tax_percentage < 0:
                raise ValidationError("Tax Percentage cannot be negative")
            elif self.tax_percentage > 100:
                raise ValidationError("Tax Percentage cannot be more than 100")

        elif self.amount:
            if self.amount < 0:
                raise ValidationError("Amount cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tax_name

    class Meta:
        verbose_name_plural  = 'Taxes'

class TaxGeneration(models.Model):

    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='taxes_generation')
    from_amount = models.DecimalField(max_digits=10, decimal_places=2)
    to_amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage =models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural  = 'Taxes Generation'

class Commission(models.Model):
    commission_code = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank = True, null  =True)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    tax = models.ManyToManyField(Tax, blank = True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def clean(self):
        if(self.commission_percentage):
            if self.commission_percentage < 0:
                raise ValidationError("Percentage cannot be negative")
            elif self.commission_percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.commission_code
    
class TransactionCode(models.Model):
    transaction_code = models.CharField(max_length=255)
    description = models.TextField(blank = True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name= 'transaction_codes')
    sub_group = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name= 'transaction_codes')
    base_rate = models.DecimalField(max_digits=8, decimal_places=2, null= True, blank = True)
    taxes  = models.ManyToManyField(Tax, blank=True)
    discount_allowed = models.BooleanField(default=False)
    is_allowance = models.BooleanField(default=False)
    allowance_code = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def clean(self):
        if(self.tax_percentage):
            if self.tax_percentage < 0:
                raise ValidationError("Percentage cannot be negative")
            elif self.tax_percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")
        if(self.commission_service_charge_percentage):
            if self.commission_service_charge_percentage < 0:
                raise ValidationError("Percentage cannot be negative")
            elif self.commission_service_charge_percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")

        if self.base_rate:
            if self.base_rate < 0:
                raise ValidationError("Base Rate cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_code

class PackageGroup(models.Model):
    package_group = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank= True, null= True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.package_group

class Package(models.Model):

    
    package_group = models.ForeignKey(PackageGroup, on_delete=models.CASCADE, related_name= 'packages')
    package_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank= True, null= True)
    begin_sell_date = models.DateField()
    end_sell_date = models.DateField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2,default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    CALCULATION_RULE_CHOICES = (
    ('Flat Rate', 'Flat Rate'),
    ('Per Adult', 'Per Adult'),
    ('Per Room', 'Per Room'),
    )
    calculation_rule = models.CharField(max_length=20, choices=CALCULATION_RULE_CHOICES)
    POSTING_RHYTHM_CHOICES = (
    ('Post Every Night', 'Post Every Night'),
    ('Post on Arrival Night', 'Post on Arrival Night'),
    # ('Post on Every X Night Starting Y Night','Post on Every X Night Starting Y Night'),
    ('Post on Certain Nights of the week','Post on Certain Nights of the week'),
    ('Post Last Night', 'Post Last Night'),
    ('Post Every Night Except Arrival Night', 'Post Every Night Except Arrival Night'),
    )
    posting_rhythm = models.CharField(max_length=50, choices=POSTING_RHYTHM_CHOICES)
    RATE_INCLUSION_CHOICES = (
    ('Included in rate', 'Included in rate'),
    ('Add Rate Separate Line', 'Add Rate Separate Line'),
    )
    rate_inclusion = models.CharField(max_length=50, choices=RATE_INCLUSION_CHOICES)
    transaction_code = models.ForeignKey(TransactionCode, on_delete=models.CASCADE, related_name='packages')
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def clean(self):
        if(self.begin_sell_date and self.end_sell_date):
            if self.begin_sell_date >  self.end_sell_date:
                raise ValidationError("Begin Sell Date cannot be more than end sell date")

        if self.base_price:
            if self.base_price < 0:
                raise ValidationError("Base Price cannot be negative")
        if self.tax_amount:
            if self.tax_amount < 0:
                raise ValidationError("Tax Amount cannot be negative")

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

    class Meta:
        verbose_name_plural = 'Rate Classes'

class RateCategory(models.Model):
    rate_class = models.ForeignKey(RateClass, on_delete=models.CASCADE,related_name='rate_categories')
    rate_category = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.rate_category

    class Meta:
        verbose_name_plural = 'Rate Categories'

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
    DAYS_APPLICABLE = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    days_applicable = MultiSelectField(choices= DAYS_APPLICABLE, blank= True, null = True)
    print_rate = models.BooleanField(default = True)
    day_use = models.BooleanField(default = False)
    discount = models.BooleanField(default = False)
    discount_amount = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null= True)
    discount_percentage = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null= True )
    complementary = models.BooleanField(default = False)
    house_use = models.BooleanField(default = False)
    is_active  = models.BooleanField(default=True)
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
    transaction_code = models.ForeignKey(TransactionCode,null=True, blank = True, on_delete=models.CASCADE, related_name='PaymentTypes') 
    is_active  = models.BooleanField(default=True)
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
    
    def clean(self):

        if self.amount:
            if self.amount < 0:
                raise ValidationError("Amount cannot be negative")

        if(self.percentage):
            if self.percentage < 0:
                raise ValidationError("Percentage cannot be negative")
            elif self.percentage > 100:
                raise ValidationError("Percentage cannot be more than 100")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.adjust_by

class TicketCategory(models.Model):
    ticket_category_code = models.CharField(max_length=255, unique= True)
    description = models.TextField(blank = True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.ticket_category_code 

    class Meta:
        verbose_name_plural = 'Ticket Categories'

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
    subject = models.CharField( max_length=255, blank = False, null=False)
    description = models.CharField(max_length=255, blank = True, null=True)
    file_upload = models.FileField(upload_to='ticket_files/', null=True,blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    agent = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE,related_name='user_tickets')
    sla_date_and_time = models.DateTimeField()
    history = HistoricalRecords()

    def clean(self):
        today = datetime.now()
        if today > self.sla_date_and_time:
                raise ValidationError("SLA date time cannot be lesser then Current date time ")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return  str(self.room.room_number) + ' ' + str(self.id)


class SharingID(models.Model):
    sharing_id = models.PositiveIntegerField(unique=True)
    number_of_reservations = models.PositiveIntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return  str(self.sharing_id)

class ReservationType(models.Model):
    reservation_type = models.CharField(max_length=100)
    is_active  = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return  self.reservation_type

class GroupReservation(models.Model):

    STATUS_CHOICES = (
        ('Enquiry', 'Enquiry'),
        ('Tentative', 'Tentative'),
        ('Definite', 'Definite'),
    )
    ORIGIN_CHOICES = (
        ('Phone', 'Phone'),
        ('Walk-in', 'Walk-in'),
        ('House use', 'House use'),
        ('Hotel Reservation Office', 'Hotel Reservation Office'),
        ('EMAIL', 'EMAIL'),
        ('ONLINE', 'ONLINE'),
    )

    block_code = models.CharField(max_length=20,null= True, blank= True)
    group_name = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null= True, related_name='group_reservations')
    arrival_date = models.DateField()
    departure_date = models.DateField()
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null= True)
    company = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null= True, blank= True, related_name='company_group_reservations')
    travel_agent = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null= True, blank= True, related_name='travel_agent_group_reservations')
    nights = models.PositiveIntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null= True, related_name='group_reservations')
    market = models.ForeignKey(MarketCode, on_delete=models.SET_NULL, null= True, related_name='group_reservations')
    origin = models.CharField(max_length=100, choices=ORIGIN_CHOICES)
    reservation_type = models.ForeignKey(ReservationType, on_delete=models.SET_NULL, null= True)
    rate_code = models.ForeignKey(RateCode,  on_delete=models.SET_NULL, null= True, related_name='group_reservations')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null= True, related_name='group_reservations', blank= True)
    pax = models.PositiveIntegerField(default=0)
    cut_off_date = models.DateField(blank=True, null= True)
    total_rooms = models.PositiveIntegerField(default=0, null = True)

    def clean(self):
        if self.block_code is None:
            if self.pk is None:
                # for creating instance 
                if self.arrival_date:
                    if self.arrival_date > self.departure_date:
                        raise ValidationError("Arrival Date cannot be more than Departure Date")
                        
                    if self.arrival_date < date.today():
                        raise ValidationError("Arrival Date cannot be less than Current Date")

                if self.departure_date:
                    if self.departure_date < date.today():
                        raise ValidationError("Departure Date cannot be less than Current Date")
            else:
                # for updating instance 
                if self.arrival_date:
                    if self.arrival_date > self.departure_date:
                        raise ValidationError("Arrival Date cannot be more than Departure Date")

            if self.total_rooms:
                
                current_date = self.arrival_date
                while current_date < self.departure_date:
                    if RoomTypeInventory.objects.get(room_type = self.room_type, date = current_date):
                        inv  = RoomTypeInventory.objects.get(room_type = self.room_type, date = current_date)
                        if((self.total_rooms > inv.number_of_available_rooms) and (inv.number_of_overbooked_rooms >= Overbooking.objects.first().overbooking_limit)):
                            raise ValidationError("The number of rooms are more than the number of available rooms in the inventory for the arrival and departure dates.")
                        current_date += timedelta(days=1)

            if self.pax:
                if self.pax < 1:
                    raise ValidationError("There must be at least 1 PAX")
            
            if self.cut_off_date:
                if self.cut_off_date <= date.today():
                    raise ValidationError("Cut Off Date cannot be less than Current Date")


            if self.rate:
                if self.rate < 0:
                    raise ValidationError("Rate cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        diff = self.departure_date - self.arrival_date 
        self.nights = diff.days
        super().save(*args, **kwargs)



    def __str__(self):
        return 'Group Reservation ID:' + str(self.id) +' ' + self.group_name.account_name

class GroupReservationRoomType(models.Model):

    group_reservation = models.ForeignKey(GroupReservation, on_delete=models.CASCADE, related_name='room_types')
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null= True, related_name='group_reservation_room_types')
    rate_code = models.ForeignKey(RateCode, on_delete=models.SET_NULL, null= True, related_name='group_reservation_room_types')
    rate_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_rooms = models.PositiveIntegerField(default=0)
    number_of_picked_rooms = models.PositiveIntegerField(blank=True, null= True, default=0)

    def clean(self):
        if self.rate_amount:
            if self.rate_amount < 0:
                raise ValidationError("Rate Amount cannot be negative")

        if self.number_of_rooms:
            
            current_date = self.group_reservation.arrival_date
            while current_date <= self.group_reservation.departure_date:
                if RoomTypeInventory.objects.get(room_type = self.room_type, date = current_date):
                    inv  = RoomTypeInventory.objects.get(room_type = self.room_type, date = current_date)
                    if((self.number_of_rooms > inv.number_of_available_rooms) and (inv.number_of_overbooked_rooms >= Overbooking.objects.first().overbooking_limit)):
                        raise ValidationError("The number of rooms are more than the number of available rooms in the inventory for the arrival and departure dates.")
                    current_date += timedelta(days=1)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Room Types for group reservation ID:' + self.group_reservation.id + ' ' + self.group_reservation.group_name.account_name

class CardDetail(models.Model):

    guest = models.ForeignKey("accounts.GuestProfile", on_delete=models.CASCADE, related_name='card_details')
    payment_type = models.ForeignKey(PaymentType,null=True, on_delete=models.SET_NULL, related_name="card_details")
    name_on_card = models.TextField()
    card_number = CardNumberField(_('card number'))
    expiry = CardExpiryField(_('expiration date'))
    cvv_cvc = SecurityCodeField(_('security code'))
    masked_card_number = models.CharField(max_length=16,blank=True, null=True)
    masked_cvv_cvc = models.CharField(max_length=3, blank=True, null=True, default='XXX')
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.masked_card_number = 'XXXXXXXXXXXX' + str(self.card_number[-4:])
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Card Details for ' + self.guest.first_name + ' ' + self.guest.last_name

class Reservation(models.Model):

    RESERVATION_STATUS_CHOICES = (
        ('Reserved', 'Reserved'),
        ('Wait-list', 'Wait-list'),
        ('Due In', 'Due In'),
        ('Checked In', 'Checked In'),
        ('Due Out', 'Due Out'),
        ('Roll Over', 'Roll Over'),
        ('Checked Out', 'Checked Out'),
        ('No Show', 'No Show'),
        ('Cancelled', 'Cancelled'),
        ('Not Reserved', 'Not Reserved'),
        ('Enquiry Only', 'Enquiry Only'),
    )
    ORIGIN_CHOICES = (
        ('Phone', 'Phone'),
        ('Walk-in', 'Walk-in'),
        ('House use', 'House use'),
        ('Hotel Reservation Office', 'Hotel Reservation Office'),
        ('EMAIL', 'EMAIL'),
        ('ONLINE', 'ONLINE'),
    )
    booking_id  = models.CharField(max_length=9,blank = True, null= True)
    guest = models.ForeignKey("accounts.GuestProfile", null=True, on_delete=models.SET_NULL, related_name='reservations')
    sharing_id = models.ForeignKey(SharingID, on_delete=models.SET_NULL, null=True, blank=True)
    arrival_date = models.DateField()
    nights = models.PositiveIntegerField(default=0)
    departure_date = models.DateField()
    adults = models.PositiveIntegerField()
    children = models.PositiveIntegerField(default=0)
    number_of_rooms = models.PositiveIntegerField()
    room_type = models.ForeignKey(RoomType,null=True, on_delete=models.SET_NULL, related_name='reservations')
    selected_room = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name='selected_room_reservations', null=True, blank=True)
    rate_code = models.ForeignKey(RateCode,null=True, on_delete=models.SET_NULL, related_name='reservations')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    room_type_to_charge = models.ForeignKey(RoomType,null=True,  on_delete=models.SET_NULL, related_name='room_to_charge_reservations', blank=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    extras = models.ManyToManyField(Extra, blank=True)
    block_code = models.ForeignKey(GroupReservation, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    eta = models.TimeField(null=True, blank=True)
    etd = models.TimeField(null=True, blank=True)
    reservation_type = models.ForeignKey(ReservationType,null =True, on_delete=models.SET_NULL, related_name='reservations')
    market = models.ForeignKey(MarketCode, null=True, on_delete=models.SET_NULL, related_name='reservations')
    source = models.ForeignKey(Source, null=True, on_delete=models.SET_NULL, related_name='reservations')
    origin = models.CharField(max_length=100, choices=ORIGIN_CHOICES)
    payment_type = models.ForeignKey(PaymentType, null=True, on_delete=models.SET_NULL, related_name='reservations')
    card_details = models.ForeignKey(CardDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default= 0)
    split_by = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey("accounts.Account", on_delete=models.SET_NULL, null=True, blank=True, related_name='company_reservations')
    agent = models.ForeignKey("accounts.Account",on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_reservations')
    booker = models.ForeignKey("accounts.Booker", on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    print_rate = models.BooleanField(default=True)
    reservation_status = models.CharField(max_length=100, choices=RESERVATION_STATUS_CHOICES)
    commission = models.BooleanField(default= False)
    po_number = models.CharField(max_length=100, blank=True, null= True)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_base_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_extra_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stay_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    travel_agent_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost_of_stay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pick_up = models.ForeignKey(PickupDropDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name='pick_up_reservations')
    drop = models.ForeignKey(PickupDropDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name='drop_reservations')
    preferences = models.ManyToManyField(Preference, blank=True)
    comments = models.TextField(blank=True)
    billing_instruction = models.TextField(blank=True)
    unique_id = models.CharField(max_length=100, blank= True, null= True)
    sub_booking_id = models.CharField(max_length=100,  blank= True, null= True)
    transaction_id = models.TextField(blank= True, null= True)
    voucher_number = models.CharField(max_length=100,  blank= True, null= True)
    do_not_move  = models.BooleanField(default = False)
    no_post = models.BooleanField(default = False)
    history  = HistoricalRecords()

    def clean(self):
        
        if self.booking_id:
            pass
        else:
            if self.pk is None:
                # for creating instance 
                if self.arrival_date:
                    if self.arrival_date > self.departure_date:
                        raise ValidationError("Arrival Date cannot be more than Departure Date")
                        
                    if self.arrival_date <= date.today():
                        raise ValidationError("Arrival Date cannot be less than Current Date")

                if self.departure_date:
                    if self.departure_date <= date.today():
                        raise ValidationError("Departure Date cannot be less than Current Date")
            else:
                # for updating instance 
                if self.arrival_date:
                    if self.arrival_date > self.departure_date:
                        raise ValidationError("Arrival Date cannot be more than Departure Date")

        if self.booking_id:
            pass
        else:
            if self.number_of_rooms:
                current_date = self.arrival_date
                while current_date <= self.departure_date:
                    if RoomTypeInventory.objects.get(room_type = self.room_type, date = current_date):
                        inv  = RoomTypeInventory.objects.get(room_type = self.room_type, date = current_date)
                        if((self.number_of_rooms > inv.number_of_available_rooms) and (inv.number_of_overbooked_rooms >= Overbooking.objects.first().overbooking_limit)):
                            raise ValidationError("The number of rooms are more than the number of available rooms in the inventory for the arrival and departure dates.")
                        current_date += timedelta(days=1)

        # if self.adults and self.children and self.number_of_rooms:
        #     if self.adults + self.children > 3*self.number_of_rooms:
        #         raise ValidationError("The sum of adults and children should be less than or equal to 3 in one room")

        if self.total_discount:
            if self.total_discount < 0:
                raise ValidationError("Total Discount cannot be negative")
        if self.total_extra_charge:
            if self.total_extra_charge < 0:
                raise ValidationError("Total Extra Charge cannot be negative")
        if self.total_tax:
            if self.total_tax < 0:
                raise ValidationError("Total Tax cannot be negative")
        if self.total_payment:
            if self.total_payment < 0:
                raise ValidationError("Total Payment cannot be negative")
        if self.stay_total:
            if self.stay_total < 0:
                raise ValidationError("Stay Total cannot be negative")
        if self.travel_agent_commission:
            if self.travel_agent_commission < 0:
                raise ValidationError("Travel Agent Commission cannot be negative")
        if self.total_cost_of_stay:
            if self.total_cost_of_stay < 0:
                raise ValidationError("Total Cost of Stay cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        # diff = self.departure_date - self.arrival_date 
        # self.nights = diff.days
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Reservation ID:' + str(self.id) +' ' + self.guest.last_name

class Folio(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='folios')
    folio_number = models.PositiveIntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    room = models.ForeignKey(Room,null=True,blank=True, on_delete=models.SET_NULL, related_name='folios')
    guest = models.ForeignKey("accounts.GuestProfile",null=True, on_delete=models.SET_NULL, related_name='folios')
    company_agent = models.ForeignKey("accounts.Account", null=True, on_delete=models.SET_NULL, related_name='folios')
    is_settled = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    # def clean(self):
    #     if self.is_settled:
    #         if self.balance != 0:
    #             raise ValidationError("Folio cannot be settled without 0 balance")

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return 'Folio Number ' +  str(self.folio_number) + ' for Reservation ID: ' + str(self.reservation.id)

class Invoice(models.Model):
    folio = models.OneToOneField(Folio, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_cancelled = models.BooleanField(default=False)

    def clean(self):
        if self.invoice_amount:
            if self.invoice_amount < 0:
                raise ValidationError('Invoice Amount cannot be negative')
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Invoice ID: ' + str(self.id) 



class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = [
        ('Bill', 'Bill'),
        ('Payment', 'Payment'),
        ('Allowance', 'Allowance'),
        ('Round off', 'Round off'),
        ('Paid out', 'Paid out')
    ]

    folio = models.ForeignKey(Folio, on_delete=models.CASCADE, related_name  = 'transactions')
    transaction_code = models.ForeignKey(TransactionCode, on_delete=models.CASCADE, related_name  = 'transactions')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name  = 'transactions')
    guest = models.ForeignKey("accounts.GuestProfile", null=True,blank = True, on_delete=models.SET_NULL, related_name='transactions')
    company_agent = models.ForeignKey("accounts.Account",null=True,blank = True,  on_delete=models.SET_NULL, related_name='transactions')
    passer_by = models.ForeignKey("accounts.PasserBy",null=True,blank = True,  on_delete=models.SET_NULL, related_name='transactions')
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(null=True, blank= True)
    room = models.ForeignKey(Room, null=True,blank = True, on_delete=models.SET_NULL, related_name='transactions')
    quantity = models.PositiveIntegerField(null= True, blank=True)
    package = models.ForeignKey(Package, null=True, blank = True, on_delete=models.SET_NULL, related_name='transactions')
    rate_code = models.ForeignKey(RateCode, null=True, blank = True, on_delete=models.SET_NULL, related_name='transactions')
    supplement = models.TextField(null=True, blank= True)
    date = models.DateTimeField()
    description = models.TextField(null=True, blank= True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank= True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank= True)
    transaction_type = models.CharField(max_length=50, choices = TRANSACTION_TYPE_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank= True)
    is_deposit = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_moved = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)
    pos_bill_number = models.CharField(max_length=255,null=True, blank= True)
    pos_session = models.CharField(max_length=255,null=True, blank= True)
    allowance_transaction = models.ForeignKey('self', null=True, blank = True, on_delete=models.SET_NULL, related_name='transactions')
    invoice = models.ForeignKey(Invoice, null=True, blank = True, on_delete=models.SET_NULL, related_name='transactions')
    card = models.ForeignKey(CardDetail, null=True, blank = True, on_delete=models.SET_NULL, related_name='transactions')

    def clean(self):

        if self.base_amount:
            if self.base_amount < 0:
                raise ValidationError("Base Amount cannot be negative")
        if self.discount_amount:
            if self.discount_amount < 0:
                raise ValidationError("Discount Amount cannot be negative")
        if(self.discount_percentage):
            if self.discount_percentage < 0:
                raise ValidationError("Discount Percentage cannot be negative")
            elif self.discount_percentage > 100:
                raise ValidationError("Disocunt Percentage cannot be more than 100")
        if(self.tax_percentage):
            if self.tax_percentage < 0:
                raise ValidationError("Tax Percentage cannot be negative")
            elif self.tax_percentage > 100:
                raise ValidationError("Tax Percentage cannot be more than 100")
        if self.cgst:
            if self.cgst < 0:
                raise ValidationError("CGST cannot be negative")
        if self.sgst:
            if self.sgst < 0:
                raise ValidationError("SGST cannot be negative")
        if self.total:
            if self.total < 0:
                raise ValidationError("Total cannot be negative")
        if(self.service_charge_commission_percentage):
            if self.service_charge_commission_percentage < 0:
                raise ValidationError("Service Charge Commission Percentage cannot be negative")
            elif self.service_charge_commission_percentage > 100:
                raise ValidationError("Service Charge Commission Percentage cannot be more than 100")
        if self.service_charge_commission:
            if self.service_charge_commission < 0:
                raise ValidationError("Service Charge Commission cannot be negative")
        if(self.service_charge_commission_tax_percentage):
            if self.service_charge_commission_tax_percentage < 0:
                raise ValidationError("Service Charge Commission Tax Percentage cannot be negative")
            elif self.service_charge_commission_tax_percentage > 100:
                raise ValidationError("Service Charge Commission Tax Percentage cannot be more than 100")
        if self.service_charge_commission_cgst:
            if self.service_charge_commission_cgst < 0:
                raise ValidationError("Service Charge Commission CGST cannot be negative")
        if self.service_charge_commission_sgst:
            if self.service_charge_commission_sgst < 0:
                raise ValidationError("Service Charge Commission SGST cannot be negative")
        if self.total_with_service_charge_commission:
            if self.total_with_service_charge_commission < 0:
                raise ValidationError("Total with Service Charge Commission cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Transaction for reservation ID: ' +str(self.id) + ' under Transaction Code: ' + self.transaction_code.transaction_code
    



class TaxTransaction(models.Model):

    tax = models.ForeignKey(Tax,null=True, on_delete=models.SET_NULL, related_name='tax_transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='tax_transactions')
    tax_amount  = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return  self.tax.tax_name + ' tax Transaction for transaction ID: ' +str(self.transaction.id) 
    
class RoomOccupancy(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='room_occupancy')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='room_occupancy')
    from_date = models.DateField()
    to_date = models.DateField()
    history = HistoricalRecords()

    def clean(self):
        if self.pk is None:
            # for creating instance 
            if self.from_date:
                if self.from_date > self.to_date:
                    raise ValidationError("From Date cannot be more than Departure Date")
                    
                if self.from_date < date.today():
                    raise ValidationError("From Date cannot be less than Current Date")

            if self.to_date:
                if self.to_date < date.today():
                    raise ValidationError("To Date cannot be less than Current Date")
        else:
            # for updating instance 
            if self.from_date:
                if self.from_date > self.to_date:
                        raise ValidationError("From Date cannot be more than To Date")

    def __str__(self):
        return 'Room Occupancy for room number: ' + str(self.room.room_number) + ' and reservation ID: ' + str(self.reservation.id)

    class Meta:
        verbose_name_plural = 'Room Occupancies'

class WaitlistManager(models.Manager):
    def add_to_waitlist(self, reservation, date):
        # Find the next available position
        last_entry = self.filter(date = date).order_by('wait_list_sequence').last()
        if last_entry:
            wait_list_sequence = last_entry.wait_list_sequence + 1
        else:
            wait_list_sequence = 1
        # Create the new entry
        entry = self.create(reservation = reservation, wait_list_sequence = wait_list_sequence, date = date)
        return entry
    
    def remove_from_waitlist(self, reservation):
        # Find the user's entry and delete it
        entry = self.get(reservation=reservation)
        entry.delete()

class WaitList(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE,unique=True)
    wait_list_sequence = models.PositiveIntegerField(db_index=True)
    date = models.DateField()
    history = HistoricalRecords()

    objects = WaitlistManager()

    def __str__(self):
        return 'Waitlist sequence: ' +  str(self.wait_list_sequence) + ' for Reservation ID: ' +  self.reservation.id

class DailyDetail(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='daily_details')
    date = models.DateField()
    room_type = models.ForeignKey(RoomType, null=True,  on_delete=models.SET_NULL, related_name= 'daily_details')
    rate_code = models.ForeignKey(RateCode, null=True,  on_delete=models.SET_NULL, related_name= 'daily_details')
    total_rate  = models.DecimalField(max_digits=10, decimal_places=2)
    room_rate  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank =True)
    package_rate =models.DecimalField(max_digits=10, decimal_places=2, null=True, blank =True)
    room = models.ForeignKey(Room, null =True, blank=True, on_delete=models.SET_NULL, related_name= 'daily_details')
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name='daily_details')
    adults = models.PositiveSmallIntegerField()
    children = models.PositiveSmallIntegerField(default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank =True)
    market = models.ForeignKey(MarketCode,null=True, blank=True, on_delete=models.SET_NULL, related_name='daily_details')
    source = models.ForeignKey(Source,null=True, blank=True, on_delete=models.SET_NULL, related_name='daily_details')
    history = HistoricalRecords()

    def clean(self):
        # if self.adults + self.children > 3:
        #         raise ValidationError("The sum of Adults and Children should not exceed 3")
        if self.total_rate:
            if self.total_rate < 0:
                raise ValidationError("Total Rate cannot be negative")
        if self.room_rate:
            if self.room_rate < 0:
                raise ValidationError("Room Rate cannot be negative")
        if self.package_rate:
            if self.package_rate < 0:
                raise ValidationError("Package Rate cannot be negative")
        if self.discount_amount:
            if self.discount_amount < 0:
                raise ValidationError("Discount Amount cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Daily Details for Reservation ID:' + str(self.reservation.id)

class DocumentType(models.Model):
    document_type  = models.CharField(max_length=255,blank = False, null=False ,unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.document_type

class Document(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE,related_name='documents')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='documents')
    invoice = models.ForeignKey(Invoice,null=True,blank=True, on_delete=models.SET_NULL,related_name='documents')
    document = models.FileField(upload_to='documents/',null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.document_type


class Alert(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='alerts')
    check_in_alert = models.TextField( blank=True, null=True)
    check_out_alert = models.TextField( blank=True, null=True)
    reservation_alert = models.TextField( blank=True, null=True)
    housekeeping_alert = models.TextField( blank=True, null=True)

    def __str__(self):
        return 'Alerts for reservation ID:' +  self.reservation.id

class RateSummary(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='rate_summaries')
    date = models.DateField()
    rate_code = models.ForeignKey(RateCode,null= True, on_delete=models.SET_NULL, related_name='rate_summaries')
    daily_detail  = models.OneToOneField(DailyDetail, on_delete=models.CASCADE, related_name='rate_summaries')
    room_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    room_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_tax_generated = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_posted  = models.BooleanField(default= False)

    def clean(self):
        if self.room_tax:
            if self.room_tax > 100:
                raise ValidationError("Percentage cannot be more than 100")
            elif self.room_tax < 0:
                raise ValidationError("Percentage cannot be negative")

        if self.room_revenue:
            if self.room_revenue < 0:
                raise ValidationError("Base Price cannot be negative")

        if self.package_revenue:
            if self.package_revenue < 0:
                raise ValidationError("Base Price cannot be negative")

        if (self.package_tax):
            if self.package_tax < 0:
                raise ValidationError("Package Tax cannot be negative")

        if (self.total_tax_generated):
            if self.total_tax_generated < 0:
                raise ValidationError("Total Tax generated  cannot be negative")

        if (self.total_tax_generated):
            if self.total_tax_generated < 0:
                raise ValidationError("Total Tax generated  cannot be negative")

        if (self.sub_total):
            if self.sub_total < 0:
                raise ValidationError("Subtotal cannot be negative")

        if (self.total):
            if self.total < 0:
                raise ValidationError("Total cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.room_revenue < 7500:
            self.room_tax = (self.room_revenue * 12 / 100)
        else:
            self.room_tax = (self.room_revenue * 18 / 100)

        if self.package_revenue:
            self.package_tax = (self.package_revenue * 18 / 100)

        self.sub_total = self.room_revenue + self.package_revenue
        self.total_tax_generated = self.room_tax + self.package_tax
        self.total = self.total_tax_generated + self.sub_total
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Rate Summary for Reservation ID: ' + str(self.reservation.id)

    class Meta:
        verbose_name_plural = 'Rate Summaries'


class OutofOrderandService(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('out_of_order', 'OutofOrder'),
        ('out_of_service', 'Out of Service')
    ]
    ROOM_STATUS_CHOICES = [
        ('clean', 'Clean'),
        ('inspected', 'Inspected'),
        ('dirty', 'Dirty')
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='out_of_order_or_out_of_service')
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=100, choices=SERVICE_STATUS_CHOICES)
    return_status = models.CharField(max_length=100, choices=ROOM_STATUS_CHOICES, default="dirty")
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE, related_name='out_of_order_or_out_of_service')
    remarks = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    def clean(self):
        if self.pk is None:
            if self.from_date:
                if self.from_date < date.today():
                    raise ValidationError("From Date needs to be more than or equal to Today")
                if self.from_date > self.to_date:
                    raise ValidationError("From Date needs to be less than or equal to To Date")
            if self.to_date:
                if self.to_date < date.today():
                    raise ValidationError("To Date needs to be more than or equal to Today")
        else:
            if self.from_date > self.to_date:
                raise ValidationError("From Date needs to be less than or equal to To Date")

    def __str__(self):
        return 'Out of Order/Out of Service for room: ' + self.room.room_number

    class Meta:
        verbose_name = 'Out of Order/Out of Service'
        verbose_name_plural = 'Out of Order/Out of Service'

class NightAudit(models.Model):
    NIGHT_AUDIT_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('not_completed', 'Not Completed')
    ]
    business_date = models.DateField()
    notes = models.CharField(max_length=255, blank=True, null=True)
    country_and_state_check = models.CharField(max_length=100, choices=NIGHT_AUDIT_STATUS_CHOICES, default="not_completed")
    arrivals_not_yet_checked_in = models.CharField(max_length=100, choices=NIGHT_AUDIT_STATUS_CHOICES, default="not_completed")
    departures_not_checked_out = models.CharField(max_length=100, choices=NIGHT_AUDIT_STATUS_CHOICES, default="not_completed")
    rolling_business_date = models.CharField(max_length=100, choices=NIGHT_AUDIT_STATUS_CHOICES, default="completed")
    posting_room_and_tax = models.CharField(max_length=100, choices=NIGHT_AUDIT_STATUS_CHOICES, default="not_completed")
    printing_reports = models.CharField(max_length=100, choices=NIGHT_AUDIT_STATUS_CHOICES, default="not_completed")
    history = HistoricalRecords()

    def __str__(self):
        return 'Night Audit for: ' +  str(self.business_date)


class Forex(models.Model):
    CURRENCY_CHOICES =[(currency.alpha_3, f"{currency.name} ({currency.alpha_3})") for currency in pycountry.currencies]

    room = models.ForeignKey(Room,null=True, on_delete=models.SET_NULL, related_name='forexes')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='forexes')
    guest = models.ForeignKey("accounts.GuestProfile", null=True, on_delete=models.SET_NULL, related_name='forexes')
    currency = models.CharField(max_length=3,choices= CURRENCY_CHOICES)
    rate_for_the_day = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    amount = models.PositiveIntegerField()
    equivalent_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    tax = models.ForeignKey(Tax, null=True,blank=True, on_delete=models.SET_NULL, related_name='forexes')
    cgst = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    sgst = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    history = HistoricalRecords()

    def clean(self):

        if self.amount < 0:
            raise ValidationError("Amount cannot be negative")
        if self.rate_for_the_day < 0:
            raise ValidationError("Ratecannot be negative")
        if self.equivalent_amount < 0:
            raise ValidationError("Equivalent Amount cannot be negative")
        if self.equivalent_amount < 0:
            raise ValidationError("Equivalent Amount cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.amount:
            self.equivalent_amount = self.rate_for_the_day * self.amount

            if self.equivalent_amount < 25000:
                self.cgst = 22.5
                self.sgst = 22.5
            else:
                self.cgst = 0.01 * self.equivalent_amount * 0.09
                self.sgst = 0.01 * self.equivalent_amount * 0.09

            self.total = (self.equivalent_amount - (self.sgst + self.cgst))
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Forex for Reservation ID: ' + str(self.reservation.id)

    class Meta:
        verbose_name_plural = 'Forex'

class FixedCharge(models.Model):

    FREQUENCY_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly','Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly','Quarterly'),
        ('yearly','Yearly') 
    ]   
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='fixed_charges')
    guest = models.ForeignKey("accounts.GuestProfile", null=True, on_delete=models.SET_NULL,related_name='fixed_charges')
    frequency =  models.CharField(max_length=100,choices=FREQUENCY_CHOICES)
    begin_date  = models.DateField()
    end_date =  models.DateField()
    transaction_code =models.ForeignKey(TransactionCode,null=True, on_delete=models.SET_NULL,related_name='fixed_charges')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()
    supplement = models.CharField(max_length=255)
    history = HistoricalRecords()

    def clean(self):
        if self.begin_date > self.end_date:
                raise ValidationError("The Begin Date Should be less than End Date")
        if self.amount < 0:
                raise ValidationError("Amount should not be negative")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Fixed Charges for Reservation ID: ' + str(self.reservation.id)


class RoutingCode(models.Model):
    routing_code = models.CharField(max_length=100,unique=True)
    description  = models.TextField(blank = True, null = True )
    transaction_codes = models.ManyToManyField(TransactionCode)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.routing_code)

class Routing(models.Model):
    ROUTING_CHOICES = [
        ('room', 'Room'),
        ('guest', 'Guest'),
        ('account', 'Account'),
        ('folio', 'Folio')
    ]
    routing_type =  models.CharField(max_length=100, choices=ROUTING_CHOICES)
    routing_code = models.ForeignKey(RoutingCode,null=True, on_delete=models.SET_NULL, related_name= 'routings')
    entry_stay = models.BooleanField(default=False)
    begin_date  = models.DateField()
    end_date =  models.DateField()
    from_room = models.ForeignKey(Room, null=True,blank = True, on_delete=models.CASCADE, related_name= 'routings_from_room')
    to_room = models.ForeignKey(Room, null=True,blank = True, on_delete=models.CASCADE, related_name= 'routings_to_room')
    to_folio = models.ForeignKey(Folio,null=True,blank = True, on_delete=models.CASCADE, related_name= 'routings')
    from_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='routings_from_reservation')
    to_reservations = models.ForeignKey(Reservation, on_delete=models.CASCADE,related_name='routings_to_reservation')
    routing_to_guest = models.ForeignKey("accounts.GuestProfile",blank = True, null=True,on_delete=models.SET_NULL,related_name='routings_to_guest')
    routing_to_account = models.ForeignKey("accounts.Account", blank = True, null=True,on_delete=models.SET_NULL,related_name='routings_to_account')
    routing_for_guest = models.ForeignKey("accounts.GuestProfile",blank = True, null=True,on_delete=models.SET_NULL,related_name='routings_for_guest')
    payment_type = models.ForeignKey(PaymentType, null=True, on_delete=models.SET_NULL, related_name= 'routings')
    transaction = models.ManyToManyField(Transaction)
    history = HistoricalRecords()

    def clean(self):
        if self.begin_date > self.end_date:
                raise ValidationError("The Begin Date Should be less than End Date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.route_to_room)

class Cancellation(models.Model):
    CANCELLATION_TYPE_CHOICES = [
        ('with_payment','With Payment'),
        ('without_payment','Without Payment')
    ]
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='cancellations')
    group_reservation = models.ForeignKey(GroupReservation, on_delete=models.CASCADE, related_name='cancellations')
    reason_code = models.ForeignKey(Reason,null=True, on_delete=models.SET_NULL, related_name='cancellations')
    remarks = models.TextField(blank=True, null=True)
    cancellation_type = models.CharField(max_length=100, choices=CANCELLATION_TYPE_CHOICES)
    payment_transaction = models.ForeignKey(Transaction,null=True, on_delete=models.SET_NULL, related_name='cancellations')
    cancellation_date = models.DateField()
    history = HistoricalRecords()

    def clean(self):

        if self.pk is None:
            # for creating instance 
            if self.cancellation_date:
                if self.cancellation_date < date.today():
                    raise ValidationError("Cancellation Date cannot be less than Current Date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def ___str__(self):
        return 'Cancellation ID:' + self.id 

class Reinstate(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reinstates')
    reason_code = models.ForeignKey(Reason, null=True, on_delete=models.SET_NULL, related_name='reinstates')
    remarks = models.TextField(blank=True, null=True)
    reinstate_date = models.DateField()
    history = HistoricalRecords()

    def clean(self):

        if self.pk is None:
            # for creating instance 
            if self.reinstate_date:
                if self.reinstate_date < date.today():
                    raise ValidationError("Reinstate Date cannot be less than Current Date")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Reinstate ID:' + self.id 

