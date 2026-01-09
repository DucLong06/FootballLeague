from django.contrib import admin
from .models import Standing


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ["rank", "team", "season", "played", "won", "drawn", "lost", "goals_for", "goals_against", "goal_diff", "points"]
    list_filter = ["season"]
    search_fields = ["team__name"]
    autocomplete_fields = ["season", "team"]
    ordering = ["season", "-points", "-goal_diff", "-goals_for"]

    actions = ["recalculate_standings"]

    def rank(self, obj):
        standings = Standing.objects.filter(season=obj.season).order_by("-points", "-goal_diff", "-goals_for")
        for i, s in enumerate(standings, 1):
            if s.id == obj.id:
                if i == 1:
                    return "🥇 1"
                elif i == 2:
                    return "🥈 2"
                elif i == 3:
                    return "🥉 3"
                return str(i)
        return "-"
    rank.short_description = "#"

    @admin.action(description="Tính lại BXH cho các đội đã chọn")
    def recalculate_standings(self, request, queryset):
        for standing in queryset:
            standing.update_stats()
        self.message_user(request, f"Đã cập nhật {queryset.count()} đội")
