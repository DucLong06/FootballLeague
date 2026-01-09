from django.contrib import admin
from .models import Season


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "start_date", "end_date", "is_active"]
    list_filter = ["type", "is_active"]
    search_fields = ["name"]
    list_editable = ["is_active"]
    date_hierarchy = "start_date"

    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("name", "type", "description")
        }),
        ("Thời gian", {
            "fields": ("start_date", "end_date")
        }),
        ("Trạng thái", {
            "fields": ("is_active",)
        }),
    )
