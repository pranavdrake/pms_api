from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from reservations.models import RateCode, Commission, Room, Preference, MarketCode, Source, Reservation
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from datetime import date

class Department(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model."""
    department = models.ForeignKey(Department,null= True, blank = True, on_delete=models.SET_NULL)
    is_account_manager = models.BooleanField(default=False)

    username = None
    email = models.EmailField(_('email address'), unique=True)
    history = HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Company', 'Company'),
        ('Travel Agent', 'Travel Agent'),
        ('Group', 'Group'),
    ]
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20,null=True, choices=ACCOUNT_TYPE_CHOICES)
    email = models.EmailField(blank = True, null= True)
    phone_number = models.CharField(max_length=20,blank = True, null= True)
    address_line_1 = models.CharField(max_length=255 ,blank = True, null= True)
    address_line_2 = models.CharField(max_length=255,blank = True, null= True)
    country = CountryField(blank = True, null= True)
    state = models.CharField(max_length=50 ,blank = True, null= True)
    city = models.CharField(max_length=50 ,blank = True, null= True)
    postal_code = models.CharField(max_length=20 ,blank = True, null= True)
    is_active = models.BooleanField(default=True)
    gst_id = models.CharField(max_length=50,blank = True, null= True)
    iata = models.CharField(max_length=50,blank = True, null= True)
    is_btc_approved = models.BooleanField(default=False)
    secondary_email = models.EmailField(blank = True, null= True)
    rate_code = models.ForeignKey(RateCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounts')
    notes = models.TextField(blank = True, null= True)
    commission = models.ForeignKey(Commission, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounts')
    account_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='account_manager_accounts')
    financial_associate = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='financial_associate_accounts')
    history = HistoricalRecords()

    def __str__(self):
        return  self.account_name

class VIP(models.Model):

    vip_level = models.PositiveSmallIntegerField()
    vip_type = models.CharField(max_length = 50)
    history = HistoricalRecords()

    def __str__(self):
        return  str(self.vip_level) + ' ' + self.vip_type

class GuestProfile(models.Model):
    # Salutation choices
    SALUTATION_CHOICES = [
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Mrs', 'Mrs'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
        ('Capt', 'Capt'),
        ('Wg Cdr', 'Wg Cdr'),
        ('Major', 'Major'),
        ('Colonel', 'Colonel'),
    ]

    # Guest Type choices
    FIT = 'FIT'
    CORPORATE = 'Corporate'
    GUEST_TYPE_CHOICES = [
        ('FIT', 'FIT'),
        ('Corporate', 'Corporate'),
    ]
    GUEST_STATUS_CHOICES = [
        ('In House', 'In House'),
        ('Out', 'Out'),
    ]

    first_name = models.CharField(max_length=255 ,blank = True, null = True)
    last_name = models.CharField(max_length=255)
    guest_status = models.CharField( max_length=255 ,choices=GUEST_STATUS_CHOICES ,default='Out')
    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES)
    address_line_1 = models.CharField(max_length=255,blank = True, null = True)
    address_line_2 = models.CharField(max_length=255, blank = True, null = True)
    country = CountryField(blank = True, null = True)
    state = models.CharField(max_length=255,  blank = True, null = True)
    city = models.CharField(max_length=255,  blank = True, null = True)
    postal_code = models.CharField(max_length=255, blank = True, null = True)
    gst_id = models.CharField(max_length=255, blank = True, null = True)
    anniversary = models.DateField( blank = True, null = True)
    vip = models.ForeignKey(VIP, blank = True, null = True, on_delete=models.SET_NULL, related_name= 'guest_profiles')
    nationality = CountryField(blank = True, null = True)
    dob = models.DateField(blank = True, null = True)
    phone_number = models.CharField(max_length=255, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    notes = models.TextField(blank = True, null = True)
    guest_preferences = models.ManyToManyField(Preference, blank = True)
    negotiated_rate = models.ForeignKey(RateCode, blank = True, null = True, on_delete=models.SET_NULL, related_name= 'negotiated_rate_guest_profiles')
    guest_type = models.CharField(blank = True, null = True, max_length=10, choices=GUEST_TYPE_CHOICES)
    company = models.ForeignKey(Account, on_delete=models.SET_NULL, blank = True, null = True, related_name= 'guest_profiles')
    last_room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank = True, null = True, related_name= 'last_room_guest_profiles')
    last_rate = models.ForeignKey(RateCode, on_delete=models.SET_NULL, blank = True, null = True, related_name= 'last_rate_guest_profiles')
    last_visit = models.DateField( blank = True, null = True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def clean(self):

        if self.dob:
            if self.dob > date.today():
                raise ValidationError("Please enter a valid date of birth")
        if self.last_visit:
            if self.last_visit > date.today():
                raise ValidationError("Last visit cannot be more than Today")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return  self.first_name + ' ' + self.last_name

class IDDetail(models.Model):
    guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE, related_name= 'id_details')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    ID_TYPE_CHOICES = (
        ('A', 'Adhaar'),
        ('P', 'Passport'),
        ('PN', 'Pan'),
    )
    id_type = models.CharField(max_length=10, choices=ID_TYPE_CHOICES)
    issue_place = models.CharField(max_length=100)
    id_file = models.FileField(upload_to='guest_ids/',null=True)
    id_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    history = HistoricalRecords()

    def clean(self):

        if self.issue_date or self.expiry_date:
            if self.issue_date > self.expiry_date:
                raise ValidationError("Issue Date cannot be grater than Expiry Date")

            if self.issue_date > date.today():
                raise ValidationError("Issue Date cannot be grater than Today")

            if self.expiry_date < date.today():
                raise ValidationError("Expiry Date cannot be less than Today ")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return  self.first_name + ' ' + self.last_name

class Booker(models.Model):
    account= models.ForeignKey(Account,on_delete=models.CASCADE,related_name='bookers')
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255,blank = True, null = True)
    address_line_2 = models.CharField(max_length=255, blank = True, null = True)
    country = CountryField(blank = True, null = True)
    city = models.CharField(max_length=255,  blank = True, null = True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name

class VisaDetail(models.Model):
    reservation = models.ForeignKey(Reservation,null=True, on_delete=models.CASCADE,related_name='visa_details')
    visa_number= models.TextField(blank=True, null=True)
    guest= models.ForeignKey(GuestProfile,on_delete=models.CASCADE,related_name='visa_details')
    issue_date = models.DateField()
    expiry_date = models.DateField()
    visa_file = models.FileField(upload_to='visa_files/',null=True) 
    history = HistoricalRecords()

    def clean(self):
        if self.issue_date > self.expiry_date:
                raise ValidationError("Expiry date should be greater than Issue_date")

        if self.issue_date > date.today():
            raise ValidationError("Issue Date cannot be grater than Today")

        if self.expiry_date < date.today():
            raise ValidationError("Expiry Date cannot be less than Today ")

    def __str__(self):
        return self.visa_number

class MembershipType(models.Model):
    membership_type = models.CharField(max_length=255 ,blank = False, null=False,unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return  self.membership_type
    
class MembershipLevel(models.Model):
    membership_level = models.CharField(max_length=255 ,blank = False, null=False,unique=True)
    history = HistoricalRecords()

    def __str__(self):
        return  self.membership_level

class Membership (models.Model):
    guest = models.ForeignKey("accounts.GuestProfile", on_delete=models.CASCADE,related_name='guest_profiles')
    membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE,related_name='membership_types')
    membership_level = models.ForeignKey(MembershipLevel, on_delete=models.CASCADE,related_name='membership_levels')
    id_number = models.CharField(max_length=255 ,blank = False, null=False,unique=True)
    name_on_card = models.CharField(max_length=255)
    joining_date = models.DateField() 
    expiry_date = models.DateField()

    def clean(self):
        if self.joining_date > self.expiry_date:
            raise ValidationError("Joining Date cannot be more than Expiry Date")
    
        if self.joining_date:
            if self.joining_date > date.today():
                raise ValidationError("Joining Date cannot be grater than Today")

        if self.expiry_date:
            if self.expiry_date < date.today():
                raise ValidationError("Expiry Date cannot be less than Today ")
                
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name_on_card

class PasserBy(models.Model):
    # Salutation choices
    MR = 'Mr.'
    MS = 'Ms.'
    MRS = 'Mrs.'
    DR = 'Dr.'
    PROF = 'Prof.'
    CAPT = 'Capt.'
    WG_CDR = 'Wg Cdr'
    MAJOR = 'Major'
    COLONEL = 'Colonel'
    SALUTATION_CHOICES = [
        (MR, 'Mr.'),
        (MS, 'Ms.'),
        (MRS, 'Mrs.'),
        (DR, 'Dr.'),
        (PROF, 'Prof.'),
        (CAPT, 'Capt.'),
        (WG_CDR, 'Wg Cdr'),
        (MAJOR, 'Major'),
        (COLONEL, 'Colonel'),
    ]
    first_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100 ,null=True, blank=True)
    salutation = models.CharField(max_length=10,null=True, blank=True ,choices=SALUTATION_CHOICES)
    phone_number = models.CharField(max_length=255, blank = True, null = True)
    email = models.EmailField(blank = True, null = True)
    market_code = models.ForeignKey(MarketCode,blank = True, null = True, on_delete=models.SET_NULL, related_name='passers_by')
    source_code = models.ForeignKey(Source,blank = True, null = True, on_delete=models.SET_NULL, related_name='passers_by')
    history = HistoricalRecords()
   
    def __str__(self):
        return  self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name_plural = 'Passers By'