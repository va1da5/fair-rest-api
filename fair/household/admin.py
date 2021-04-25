from django.contrib import admin

from fair.tasks.models import Task

from .models import Household, HouseholdUser


class TasksInline(admin.StackedInline):
    model = Task
    verbose_name_plural = "task"
    readonly_fields = ("uuid",)
    exclude = ("deleted_at",)
    filter_horizontal = ("handlers",)
    extra = 0

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super(TasksInline, self).formfield_for_dbfield(
            db_field, request, **kwargs
        )

        if db_field.name == "handlers":
            field.queryset = field.queryset.filter(
                household=Household.objects.filter(
                    pk=request.resolver_match.kwargs.get("object_id")
                ).get()
            )

        return field


class HouseholdAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (TasksInline,)
    list_display = ("uuid", "name", "created_at")
    readonly_fields = ("uuid",)
    filter_horizontal = ("members",)


class HouseholdUserAdmin(admin.ModelAdmin):
    list_display = ("user", "max_scheduled_tasks")


admin.site.register(Household, HouseholdAdmin)
admin.site.register(HouseholdUser, HouseholdUserAdmin)
