from django.db import models
from rest_framework import serializers
from players.models import Player
from seasons.models import Season
from teams.models import Team, TeamPlayer
from matches.models import Match, Goal, Card, PlayerMatchStat
from stats.models import Standing


class PlayerSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ["id", "name", "nickname", "email", "avatar_url", "is_active", "created_at"]

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class PlayerDetailSerializer(PlayerSerializer):
    stats = serializers.SerializerMethodField()
    awards = serializers.SerializerMethodField()

    class Meta(PlayerSerializer.Meta):
        fields = PlayerSerializer.Meta.fields + ["stats", "awards"]

    def get_stats(self, obj):
        from stats.services import PlayerStatsService
        return PlayerStatsService.get_player_stats(obj)

    def get_awards(self, obj):
        # Trả về danh hiệu mà cầu thủ này đang giữ
        from stats.services import AwardsService
        all_awards = AwardsService.get_player_awards()
        player_awards = []
        for award in all_awards.get("glory", []) + all_awards.get("shame", []):
            if award["player"].id == obj.id:
                player_awards.append({
                    "icon": award["icon"],
                    "title": award["title"],
                    "description": award["description"],
                })
        return player_awards


class SeasonSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    match_count = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = ["id", "name", "type", "type_display", "start_date", "end_date", "is_active", "description", "match_count"]

    def get_match_count(self, obj):
        return obj.matches.count()


class TeamSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    player_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "name", "logo_url", "color", "player_count"]

    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

    def get_player_count(self, obj):
        return obj.players.count()


class TeamPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    position_display = serializers.CharField(source="get_position_display", read_only=True)

    class Meta:
        model = TeamPlayer
        fields = ["id", "player", "jersey_number", "position", "position_display", "is_captain"]


class TeamDetailSerializer(TeamSerializer):
    players = TeamPlayerSerializer(many=True, read_only=True)
    season = SeasonSerializer(read_only=True)

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ["season", "players"]


class GoalSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source="player.name", read_only=True)
    assist_by_name = serializers.CharField(source="assist_by.name", read_only=True)
    goal_type_display = serializers.CharField(source="get_goal_type_display", read_only=True)

    class Meta:
        model = Goal
        fields = ["id", "player", "player_name", "assist_by", "assist_by_name", "minute", "goal_type", "goal_type_display"]


class CardSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source="player.name", read_only=True)
    card_type_display = serializers.CharField(source="get_card_type_display", read_only=True)

    class Meta:
        model = Card
        fields = ["id", "player", "player_name", "card_type", "card_type_display", "minute", "reason"]


class MatchSerializer(serializers.ModelSerializer):
    season_name = serializers.CharField(source="season.name", read_only=True)
    home_team_name = serializers.CharField(source="home_team.name", read_only=True)
    away_team_name = serializers.CharField(source="away_team.name", read_only=True)
    goal_count = serializers.SerializerMethodField()
    card_count = serializers.SerializerMethodField()
    home_score = serializers.SerializerMethodField()
    away_score = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            "id", "season", "season_name", "match_date", "venue", "round",
            "home_team", "home_team_name", "away_team", "away_team_name",
            "home_score", "away_score", "notes", "goal_count", "card_count"
        ]

    def get_goal_count(self, obj):
        return obj.goals.count()

    def get_card_count(self, obj):
        return obj.cards.count()
    
    def get_home_score(self, obj):
        # Nếu có sẵn thì dùng, không thì tính từ goals
        if hasattr(obj, '_home_score') and obj._home_score is not None:
            return obj._home_score
        if obj.home_team:
            return obj.goals.filter(for_team=obj.home_team).exclude(goal_type="OWN_GOAL").count()
        return 0
    
    def get_away_score(self, obj):
        if hasattr(obj, '_away_score') and obj._away_score is not None:
            return obj._away_score
        if obj.away_team:
            return obj.goals.filter(for_team=obj.away_team).exclude(goal_type="OWN_GOAL").count()
        return 0


class MatchDetailSerializer(MatchSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    cards = CardSerializer(many=True, read_only=True)
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)

    class Meta(MatchSerializer.Meta):
        fields = MatchSerializer.Meta.fields + ["goals", "cards"]


class StandingSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    rank = serializers.SerializerMethodField()
    form = serializers.SerializerMethodField()

    class Meta:
        model = Standing
        fields = [
            "id", "rank", "team", "played", "won", "drawn", "lost",
            "goals_for", "goals_against", "goal_diff", "points", "form"
        ]

    def get_rank(self, obj):
        standings = Standing.objects.filter(season=obj.season).order_by("-points", "-goal_diff", "-goals_for")
        for i, s in enumerate(standings, 1):
            if s.id == obj.id:
                return i
        return 0

    def get_form(self, obj):
        """Lấy phong độ 5 trận gần nhất - tính từ Goals"""
        from matches.models import Match, Goal
        
        # Lấy tất cả matches của team trong season
        matches = Match.objects.filter(
            season=obj.season
        ).filter(
            models.Q(home_team=obj.team) | models.Q(away_team=obj.team)
        ).order_by("-match_date")[:5]
        
        form = []
        for match in matches:
            # Tính score từ Goals
            home_goals = Goal.objects.filter(
                match=match, 
                for_team=match.home_team
            ).exclude(goal_type="OWN_GOAL").count()
            
            away_goals = Goal.objects.filter(
                match=match, 
                for_team=match.away_team
            ).exclude(goal_type="OWN_GOAL").count()
            
            if match.home_team == obj.team:
                if home_goals > away_goals:
                    form.append("W")
                elif home_goals == away_goals:
                    form.append("D")
                else:
                    form.append("L")
            else:
                if away_goals > home_goals:
                    form.append("W")
                elif away_goals == home_goals:
                    form.append("D")
                else:
                    form.append("L")
        
        return form


class PlayerStatsSerializer(serializers.Serializer):
    """Serializer cho thống kê cầu thủ"""
    player = PlayerSerializer()
    matches_played = serializers.IntegerField()
    minutes_played = serializers.IntegerField()
    goals = serializers.IntegerField()
    own_goals = serializers.IntegerField()
    assists = serializers.IntegerField()
    yellow_cards = serializers.IntegerField()
    red_cards = serializers.IntegerField()
    clean_sheets = serializers.IntegerField()
    goals_conceded = serializers.IntegerField()
    goal_ratio = serializers.FloatField()
    contribution = serializers.IntegerField()


class AwardSerializer(serializers.Serializer):
    """Serializer cho danh hiệu"""
    key = serializers.CharField(required=False)
    icon = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    player = PlayerSerializer(required=False)
    team = TeamSerializer(required=False)
    value = serializers.FloatField()
    stat = serializers.CharField(required=False)


class OverviewSerializer(serializers.Serializer):
    """Serializer cho trang Overview"""
    total_players = serializers.IntegerField()
    total_matches = serializers.IntegerField()
    total_goals = serializers.IntegerField()
    total_cards = serializers.IntegerField()
    yellow_cards = serializers.IntegerField()
    red_cards = serializers.IntegerField()
    current_season = SeasonSerializer(required=False, allow_null=True)
    top_scorers = serializers.ListField()
    top_assists = serializers.ListField()
    top_cards = serializers.ListField()
    glory_awards = AwardSerializer(many=True)
    shame_awards = AwardSerializer(many=True)
