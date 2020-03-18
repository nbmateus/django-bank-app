from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)