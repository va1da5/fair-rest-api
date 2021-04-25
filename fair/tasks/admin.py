from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from fair.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "name",
        "description",
        "household",
        "interval",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("uuid", "created_at", "updated_at", "deleted_at")
    list_filter = ("household",)
    filter_horizontal = ("handlers",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super(TaskAdmin, self).formfield_for_dbfield(
            db_field, request, **kwargs
        )

        if db_field.name == "handlers":
            task = Task.objects.filter(
                pk=request.resolver_match.kwargs.get("object_id")
            ).get()
            field.queryset = task.household.members

        return field


admin.site.register(Task, TaskAdmin)
