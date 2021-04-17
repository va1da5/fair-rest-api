from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms

from fair.tasks.models import Task, TaskPool


class TaskPoolInline(admin.StackedInline):
    model = TaskPool
    can_delete = False
    verbose_name_plural = "taskpool"
    filter_horizontal = ("tasks",)


class UserAdmin(BaseUserAdmin):
    inlines = (TaskPoolInline,)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "name",
        "description",
        "interval",
        "created_at",
        "updated_at",
    )


admin.site.register(Task, TaskAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
