from django.contrib import admin
from accounts.models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','department')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_account_manager',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Department, SimpleHistoryAdmin)
admin.site.register(Account, SimpleHistoryAdmin)
admin.site.register(VIP, SimpleHistoryAdmin)
admin.site.register(GuestProfile, SimpleHistoryAdmin)
admin.site.register(IDDetail, SimpleHistoryAdmin)
admin.site.register(Booker, SimpleHistoryAdmin)
admin.site.register(VisaDetail, SimpleHistoryAdmin)
admin.site.register(MembershipType, SimpleHistoryAdmin)
admin.site.register(MembershipLevel, SimpleHistoryAdmin)
admin.site.register(Membership, SimpleHistoryAdmin)
admin.site.register(PasserBy, SimpleHistoryAdmin)