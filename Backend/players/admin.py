from django.contrib import admin
from django.utils.html import format_html
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "nickname", "avatar_preview", "email", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "nickname", "email"]
    list_editable = ["is_active"]
    readonly_fields = ["id", "created_at", "avatar_preview_large"]

    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("name", "nickname", "email")
        }),
        ("Ảnh đại diện", {
            "fields": ("avatar", "avatar_preview_large")
        }),
        ("Trạng thái", {
            "fields": ("is_active",)
        }),
        ("Thông tin hệ thống", {
            "fields": ("id", "created_at"),
            "classes": ("collapse",)
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return "❌"
    avatar_preview.short_description = "Avatar"

    def avatar_preview_large(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius: 10px; object-fit: cover;" />',
                obj.avatar.url
            )
        return "Chưa có ảnh"
    avatar_preview_large.short_description = "Xem trước"
