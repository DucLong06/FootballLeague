from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from players.models import Player
from seasons.models import Season
from teams.models import Team
from matches.models import Match
from stats.models import Standing
from stats.services import PlayerStatsService, AwardsService, OverviewService

from .serializers import (
    PlayerSerializer, PlayerDetailSerializer,
    SeasonSerializer,
    TeamSerializer, TeamDetailSerializer,
    MatchSerializer, MatchDetailSerializer,
    StandingSerializer,
    AwardSerializer,
)


class OverviewAPIView(APIView):
    """API Overview - Trang chủ"""

    def get(self, request):
        stats = OverviewService.get_overview_stats()
        current_season = OverviewService.get_current_season()
        top_scorers = OverviewService.get_top_scorers(10)
        top_assists = OverviewService.get_top_assists(10)
        top_cards = OverviewService.get_top_cards(10)
        awards = AwardsService.get_player_awards()

        # Serialize players in top lists
        serialized_scorers = [
            {
                "player": PlayerSerializer(item["player"], context={"request": request}).data,
                "goals": item["goals"]
            }
            for item in top_scorers
        ]
        serialized_assists = [
            {
                "player": PlayerSerializer(item["player"], context={"request": request}).data,
                "assists": item["assists"]
            }
            for item in top_assists
        ]
        serialized_cards = [
            {
                "player": PlayerSerializer(item["player"], context={"request": request}).data,
                "yellow": item["yellow"],
                "red": item["red"],
                "total": item["total"]
            }
            for item in top_cards
        ]

        # Serialize awards
        glory_awards = [
            {
                "key": award.get("key"),
                "icon": award["icon"],
                "title": award["title"],
                "description": award["description"],
                "player": PlayerSerializer(award["player"], context={"request": request}).data,
                "value": award["value"],
                "stat": award.get("stat"),
            }
            for award in awards.get("glory", [])
        ]
        shame_awards = [
            {
                "key": award.get("key"),
                "icon": award["icon"],
                "title": award["title"],
                "description": award["description"],
                "player": PlayerSerializer(award["player"], context={"request": request}).data,
                "value": award["value"],
                "stat": award.get("stat"),
            }
            for award in awards.get("shame", [])
        ]

        return Response({
            "total_players": stats["total_players"],
            "total_matches": stats["total_matches"],
            "total_goals": stats["total_goals"],
            "total_cards": stats["total_cards"],
            "yellow_cards": stats["yellow_cards"],
            "red_cards": stats["red_cards"],
            "current_season": SeasonSerializer(current_season).data if current_season else None,
            "top_scorers": serialized_scorers,
            "top_assists": serialized_assists,
            "top_cards": serialized_cards,
            "glory_awards": glory_awards,
            "shame_awards": shame_awards,
        })


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """API Players"""
    queryset = Player.objects.filter(is_active=True)
    serializer_class = PlayerSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayerDetailSerializer
        return PlayerSerializer

    def list(self, request, *args, **kwargs):
        """Danh sách cầu thủ kèm thống kê"""
        season_id = request.query_params.get("season")
        season = None
        if season_id:
            season = get_object_or_404(Season, pk=season_id)
            
        stats = PlayerStatsService.get_all_players_stats(season)
        
        # Serialize and combine
        result = []
        for item in stats:
            data = PlayerSerializer(item["player"], context={"request": request}).data
            data.update({k: v for k, v in item.items() if k != "player"})
            result.append(data)
            
        # Sort by name default
        result.sort(key=lambda x: x["name"])
        
        return Response(result)

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        """Thống kê chi tiết cầu thủ"""
        player = self.get_object()
        season_id = request.query_params.get("season")
        season = None
        if season_id:
            season = get_object_or_404(Season, pk=season_id)
        
        stats = PlayerStatsService.get_player_stats(player, season)
        return Response(stats)

    @action(detail=True, methods=["get"])
    def matches(self, request, pk=None):
        """Lịch sử trận đấu của cầu thủ"""
        player = self.get_object()
        matches = Match.objects.filter(player_stats__player=player).distinct().order_by("-match_date")[:20]
        serializer = MatchSerializer(matches, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def rankings(self, request):
        """Xếp hạng cầu thủ theo tiêu chí - bao gồm đầy đủ stats"""
        stat_type = request.query_params.get("type", "goals")
        season_id = request.query_params.get("season")
        limit = int(request.query_params.get("limit", 10))
        
        season = None
        if season_id:
            season = get_object_or_404(Season, pk=season_id)

        # Lấy tất cả stats của mỗi cầu thủ
        from stats.services import PlayerStatsService
        all_player_stats = PlayerStatsService.get_all_players_stats(season)
        
        # Sắp xếp theo tiêu chí
        if stat_type == "goals":
            all_player_stats.sort(key=lambda x: (-x["goals"], -x["contribution"]))
        elif stat_type == "assists":
            all_player_stats.sort(key=lambda x: (-x["assists"], -x["contribution"]))
        elif stat_type == "cards":
            all_player_stats.sort(key=lambda x: (-x["red_cards"], -x["yellow_cards"]))
        else:
            all_player_stats.sort(key=lambda x: (-x["goals"], -x["contribution"]))
        
        # Lọc chỉ những người có hoạt động
        filtered = [s for s in all_player_stats if s["goals"] > 0 or s["assists"] > 0 or s["yellow_cards"] > 0 or s["red_cards"] > 0]
        
        result = []
        for i, item in enumerate(filtered[:limit]):
            # Xác định value dựa trên type
            value = 0
            if stat_type == "goals":
                value = item["goals"]
            elif stat_type == "assists":
                value = item["assists"]
            elif stat_type == "cards":
                value = item["red_cards"] * 100 + item["yellow_cards"] # Logic tạm cho cards
            else:
                value = item["goals"]

            # Serialize player và inject stats vào player object để frontend dùng
            player_data = PlayerSerializer(item["player"], context={"request": request}).data
            player_data["matches_played"] = item["matches_played"]

            result.append({
                "rank": i + 1,
                "player": player_data,
                "value": value,
                "goals": item["goals"],
                "assists": item["assists"],
                "yellow_cards": item["yellow_cards"],
                "red_cards": item["red_cards"],
                "contribution": item["contribution"],
                "matches_played": item["matches_played"],
            })

        return Response(result)


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """API Seasons"""
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    @action(detail=False, methods=["get"])
    def current(self, request):
        """Mùa giải hiện tại"""
        season = Season.objects.filter(is_active=True).first()
        if not season:
            return Response({"error": "No active season"}, status=status.HTTP_404_NOT_FOUND)
        return Response(SeasonSerializer(season).data)

    @action(detail=True, methods=["get"])
    def matches(self, request, pk=None):
        """Các trận của mùa"""
        season = self.get_object()
        matches = season.matches.all().order_by("-match_date")
        serializer = MatchSerializer(matches, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        """Thống kê chi tiết mùa giải"""
        from stats.services import SeasonStatsService
        
        season = self.get_object()
        stats = SeasonStatsService.get_season_stats(season)
        top_scorers = SeasonStatsService.get_season_top_scorers(season, 10)
        top_assists = SeasonStatsService.get_season_top_assists(season, 10)
        top_cards = SeasonStatsService.get_season_top_cards(season, 10)
        
        return Response({
            "season": SeasonSerializer(season).data,
            "total_players": stats["total_players"],
            "total_matches": stats["total_matches"],
            "total_goals": stats["total_goals"],
            "total_own_goals": stats["total_own_goals"],
            "total_cards": stats["total_cards"],
            "yellow_cards": stats["yellow_cards"],
            "red_cards": stats["red_cards"],
            "avg_goals_per_match": stats["avg_goals_per_match"],
            "braces": stats["braces"],
            "hat_tricks": stats["hat_tricks"],
            "pokers": stats["pokers"],
            "best_match": MatchDetailSerializer(stats["best_match"], context={"request": request}).data if stats["best_match"] else None,
            "best_match_goals": stats["best_match_goals"],
            "worst_match": MatchDetailSerializer(stats["worst_match"], context={"request": request}).data if stats["worst_match"] else None,
            "worst_match_cards": stats["worst_match_cards"],
            "team_most_goals": TeamSerializer(stats["team_most_goals"], context={"request": request}).data if stats["team_most_goals"] else None,
            "team_most_goals_count": stats["team_most_goals_count"],
            "team_most_cards": TeamSerializer(stats["team_most_cards"], context={"request": request}).data if stats["team_most_cards"] else None,
            "team_most_cards_count": stats["team_most_cards_count"],
            "top_scorers": [
                {
                    "player": PlayerSerializer(item["player"], context={"request": request}).data,
                    "goals": item["goals"]
                }
                for item in top_scorers
            ],
            "top_assists": [
                {
                    "player": PlayerSerializer(item["player"], context={"request": request}).data,
                    "assists": item["assists"]
                }
                for item in top_assists
            ],
            "top_cards": [
                {
                    "player": PlayerSerializer(item["player"], context={"request": request}).data,
                    "yellow": item["yellow"],
                    "red": item["red"],
                    "total": item["total"]
                }
                for item in top_cards
            ],
        })


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """API Teams"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeamDetailSerializer
        return TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        season_id = self.request.query_params.get("season")
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        return queryset


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """API Matches"""
    queryset = Match.objects.all().order_by("-match_date")
    serializer_class = MatchSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MatchDetailSerializer
        return MatchSerializer

    def get_queryset(self):
        queryset = Match.objects.all().order_by("-match_date")
        season_id = self.request.query_params.get("season")
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        return queryset

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """Trận gần đây"""
        limit = int(request.query_params.get("limit", 5))
        matches = self.get_queryset()[:limit]
        serializer = MatchDetailSerializer(matches, many=True, context={"request": request})
        return Response(serializer.data)


class StandingViewSet(viewsets.ReadOnlyModelViewSet):
    """API Standings"""
    queryset = Standing.objects.all()
    serializer_class = StandingSerializer

    def get_queryset(self):
        queryset = Standing.objects.all().order_by("-points", "-goal_diff", "-goals_for")
        season_id = self.request.query_params.get("season")
        if season_id:
            queryset = queryset.filter(season_id=season_id)
        return queryset

    @action(detail=False, methods=["get"])
    def current(self, request):
        """BXH mùa giải hiện tại"""
        current_season = Season.objects.filter(is_active=True, type="LEAGUE").first()
        if not current_season:
            return Response({"error": "No active league season"}, status=status.HTTP_404_NOT_FOUND)
        
        standings = Standing.objects.filter(season=current_season).order_by("-points", "-goal_diff", "-goals_for")
        serializer = StandingSerializer(standings, many=True, context={"request": request})
        return Response({
            "season": SeasonSerializer(current_season).data,
            "standings": serializer.data
        })


class AwardsAPIView(APIView):
    """API Awards"""

    def get(self, request):
        season_id = request.query_params.get("season")
        season = None
        if season_id:
            season = get_object_or_404(Season, pk=season_id)

        player_awards = AwardsService.get_player_awards(season)
        
        result = {
            "glory_awards": [
                {
                    "key": award.get("key"),
                    "icon": award["icon"],
                    "title": award["title"],
                    "description": award["description"],
                    "player": PlayerSerializer(award["player"], context={"request": request}).data,
                    "value": award["value"],
                    "stat": award.get("stat"),
                }
                for award in player_awards.get("glory", [])
            ],
            "shame_awards": [
                {
                    "key": award.get("key"),
                    "icon": award["icon"],
                    "title": award["title"],
                    "description": award["description"],
                    "player": PlayerSerializer(award["player"], context={"request": request}).data,
                    "value": award["value"],
                    "stat": award.get("stat"),
                }
                for award in player_awards.get("shame", [])
            ],
        }

        # Team awards nếu có season League
        if season and season.type == "LEAGUE":
            team_awards = AwardsService.get_team_awards(season)
            result["team_awards"] = [
                {
                    "icon": award["icon"],
                    "title": award["title"],
                    "description": award["description"],
                    "team": TeamSerializer(award["team"], context={"request": request}).data,
                    "value": award["value"],
                }
                for award in team_awards
            ]

        return Response(result)
