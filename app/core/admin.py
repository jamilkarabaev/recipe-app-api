from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):

    
    """ admin:core_user_changelist """
    ordering = ['id']
    list_display = ['email', 'name']


    """ admin:core_user_change """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}))


    """ admin:core_user_add """
    add_fieldsets= (
        (None, {'classes' : ('wide',),   'fields' : ('email', 'password1', 'password2')}),

    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)

