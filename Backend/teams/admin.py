from django.contrib import admin
from django.utils.html import format_html
from .models import Team, TeamPlayer


class TeamPlayerInline(admin.TabularInline):
    model = TeamPlayer
    extra = 1
    autocomplete_fields = ["player"]
    fields = ["player", "jersey_number", "position", "is_captain"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "season", "logo_preview", "color", "player_count"]
    list_filter = ["season"]
    search_fields = ["name"]
    autocomplete_fields = ["season"]
    inlines = [TeamPlayerInline]

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 5px; object-fit: cover;" />',
                obj.logo.url
            )
        return "❌"
    logo_preview.short_description = "Logo"

    def player_count(self, obj):
        return obj.players.count()
    player_count.short_description = "Số cầu thủ"


@admin.register(TeamPlayer)
class TeamPlayerAdmin(admin.ModelAdmin):
    list_display = ["player", "team", "jersey_number", "position", "is_captain"]
    list_filter = ["team", "position", "is_captain"]
    search_fields = ["player__name"]
    autocomplete_fields = ["team", "player"]
