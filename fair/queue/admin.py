from django.contrib import admin

from .models import QueueItem


class QueueItemAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "user",
        "task",
        "state",
        "scheduled_at",
        "activated_at",
        "postponed_at",
    )
    fields = (
        "state",
        "user",
        "task",
        "uuid",
        "stars",
        "postpone_counter",
        "scheduled_at",
        "activated_at",
        "postponed_at",
        "completed_at",
    )
    readonly_fields = (
        "uuid",
        "stars",
        "postpone_counter",
        "scheduled_at",
        "activated_at",
        "postponed_at",
        "completed_at",
    )


admin.site.register(QueueItem, QueueItemAdmin)
