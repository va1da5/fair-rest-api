from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from fair.users.models import Account


class CustomUserInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = "account"
    filter_horizontal = ("tasks",)


class UserAdmin(BaseUserAdmin):
    inlines = (CustomUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
