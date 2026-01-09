from django.contrib import admin
from .models import Match, Goal, Card, PlayerMatchStat


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 1
    autocomplete_fields = ["player", "assist_by", "for_team"]
    fields = ["player", "minute", "goal_type", "assist_by", "for_team"]


class CardInline(admin.TabularInline):
    model = Card
    extra = 0
    autocomplete_fields = ["player"]
    fields = ["player", "card_type", "minute", "reason"]


class PlayerMatchStatInline(admin.TabularInline):
    model = PlayerMatchStat
    extra = 1
    autocomplete_fields = ["player", "team"]
    fields = ["player", "team", "is_starter", "minutes_played", "is_goalkeeper", "clean_sheet", "goals_conceded", "saves"]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ["__str__", "season", "match_date", "venue", "round", "goal_count", "card_count"]
    list_filter = ["season", "match_date"]
    search_fields = ["home_team__name", "away_team__name", "venue"]
    autocomplete_fields = ["season", "home_team", "away_team"]
    date_hierarchy = "match_date"
    inlines = [GoalInline, CardInline, PlayerMatchStatInline]

    fieldsets = (
        ("Thông tin trận đấu", {
            "fields": ("season", "match_date", "venue", "round")
        }),
        ("Đội bóng (League)", {
            "fields": ("home_team", "away_team"),
            "classes": ("collapse",),
            "description": "Chỉ điền nếu là giải đấu có đội"
        }),
        ("Tỷ số (League)", {
            "fields": ("home_score", "away_score"),
            "classes": ("collapse",)
        }),
        ("Ghi chú", {
            "fields": ("notes",),
            "classes": ("collapse",)
        }),
    )

    def goal_count(self, obj):
        count = obj.goals.count()
        return f"⚽ {count}" if count > 0 else "-"
    goal_count.short_description = "Bàn thắng"

    def card_count(self, obj):
        yellow = obj.cards.filter(card_type="YELLOW").count()
        red = obj.cards.filter(card_type="RED").count()
        if yellow == 0 and red == 0:
            return "-"
        result = []
        if yellow > 0:
            result.append(f"🟨{yellow}")
        if red > 0:
            result.append(f"🟥{red}")
        return " ".join(result)
    card_count.short_description = "Thẻ"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ["player", "match", "minute", "goal_type", "assist_by"]
    list_filter = ["goal_type", "match__season"]
    search_fields = ["player__name", "assist_by__name"]
    autocomplete_fields = ["match", "player", "assist_by", "for_team"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["player", "match", "card_type", "minute", "reason"]
    list_filter = ["card_type", "match__season"]
    search_fields = ["player__name", "reason"]
    autocomplete_fields = ["match", "player"]


@admin.register(PlayerMatchStat)
class PlayerMatchStatAdmin(admin.ModelAdmin):
    list_display = ["player", "match", "team", "is_starter", "minutes_played", "is_goalkeeper", "clean_sheet"]
    list_filter = ["is_starter", "is_goalkeeper", "clean_sheet", "match__season"]
    search_fields = ["player__name"]
    autocomplete_fields = ["match", "player", "team"]
