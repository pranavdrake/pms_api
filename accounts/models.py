from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from reservations.models import RateCode, Commission, Room, Preference
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

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
        ('company', 'Company'),
        ('travel_agent', 'Travel Agent'),
        ('group', 'Group'),
    ]
    account_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
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
        return  self.vip_level + ' ' + self.vip_type

class GuestProfile(models.Model):
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

    # Guest Type choices
    FIT = 'FIT'
    CORPORATE = 'Corporate'
    GUEST_TYPE_CHOICES = [
        (FIT, 'FIT'),
        (CORPORATE, 'Corporate'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES)
    address_line_1 = models.CharField(max_length=255,blank = True, null = True)
    address_line_2 = models.CharField(max_length=255, blank = True, null = True)
    country = CountryField(blank = True, null = True)
    city = models.CharField(max_length=255,  blank = True, null = True)
    postal_code = models.CharField(max_length=255, blank = True, null = True)
    gst_id = models.CharField(max_length=255, blank = True, null = True)
    anniversary = models.DateField( blank = True, null = True)
    vip = models.ForeignKey(VIP, blank = True, null = True, on_delete=models.SET_NULL, related_name= 'guest_profiles')
    nationality = CountryField(blank = True, null = True)
    dob = models.DateField(blank = True, null = True)
    phone_number = models.CharField(max_length=255, blank = True, null = True)
    email = models.EmailField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True)
    guest_preferences = models.ManyToManyField(Preference, blank = True)
    negotiated_rate = models.ForeignKey(RateCode, blank = True, null = True, on_delete=models.SET_NULL, related_name= 'negotiated_rate_guest_profiles')
    guest_type = models.CharField(blank = True, null = True, max_length=10, choices=GUEST_TYPE_CHOICES)
    company = models.ForeignKey(Account, on_delete=models.SET_NULL, blank = True, null = True, related_name= 'guest_profiles')
    last_room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank = True, null = True, related_name= 'last_room_guest_profiles')
    last_rate = models.ForeignKey(RateCode, on_delete=models.SET_NULL, blank = True, null = True, related_name= 'last_rate_guest_profiles')
    last_visit = models.DateField( blank = True, null = True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return  self.first_name + ' ' + self.last_name

