"""
Services cho tính toán thống kê và danh hiệu
"""
from django.db.models import Count, Sum, Q, F
from django.db.models.functions import Coalesce

from players.models import Player
from matches.models import Match, Goal, Card, PlayerMatchStat
from seasons.models import Season
from teams.models import Team
from stats.models import Standing


class PlayerStatsService:
    """Service tính thống kê cầu thủ"""

    @staticmethod
    def get_player_stats(player, season=None):
        """Lấy thống kê của một cầu thủ"""
        goals_qs = player.goals.all()
        assists_qs = player.assists.all()
        cards_qs = player.cards.all()
        match_stats_qs = player.match_stats.all()

        if season:
            goals_qs = goals_qs.filter(match__season=season)
            assists_qs = assists_qs.filter(match__season=season)
            cards_qs = cards_qs.filter(match__season=season)
            match_stats_qs = match_stats_qs.filter(match__season=season)

        total_goals = goals_qs.exclude(goal_type="OWN_GOAL").count()
        own_goals = goals_qs.filter(goal_type="OWN_GOAL").count()
        assists = assists_qs.count()
        yellow_cards = cards_qs.filter(card_type="YELLOW").count()
        red_cards = cards_qs.filter(card_type="RED").count()
        
        # Tính matches_played từ cả match_stats VÀ goals/assists/cards
        # Một cầu thủ coi như đã ra sân nếu có: match_stat HOẶC goal HOẶC assist HOẶC card
        from matches.models import Match
        match_ids = set()
        match_ids.update(match_stats_qs.values_list('match_id', flat=True))
        match_ids.update(goals_qs.values_list('match_id', flat=True))
        match_ids.update(assists_qs.values_list('match_id', flat=True))
        match_ids.update(cards_qs.values_list('match_id', flat=True))
        matches_played = len(match_ids)
        
        minutes_played = match_stats_qs.aggregate(
            total=Coalesce(Sum("minutes_played"), 0)
        )["total"]
        clean_sheets = match_stats_qs.filter(is_goalkeeper=True, clean_sheet=True).count()
        goals_conceded = match_stats_qs.filter(is_goalkeeper=True).aggregate(
            total=Coalesce(Sum("goals_conceded"), 0)
        )["total"]

        goal_ratio = total_goals / matches_played if matches_played > 0 else 0
        contribution = total_goals + assists

        return {
            "matches_played": matches_played,
            "minutes_played": minutes_played,
            "goals": total_goals,
            "own_goals": own_goals,
            "assists": assists,
            "yellow_cards": yellow_cards,
            "red_cards": red_cards,
            "clean_sheets": clean_sheets,
            "goals_conceded": goals_conceded,
            "goal_ratio": round(goal_ratio, 2),
            "contribution": contribution,
        }

    @staticmethod
    def get_all_players_stats(season=None):
        """Lấy thống kê tất cả cầu thủ"""
        players = Player.objects.filter(is_active=True)
        stats_list = []
        
        for player in players:
            stats = PlayerStatsService.get_player_stats(player, season)
            stats["player"] = player
            stats_list.append(stats)
        
        return stats_list


class AwardsService:
    """Service tính danh hiệu"""

    # Danh hiệu vinh quang
    GLORY_AWARDS = {
        "top_scorer": {
            "icon": "👑",
            "title": "Vua Phá Lưới",
            "description": "Cỗ máy hủy diệt - Thủ môn nào cũng khóc!",
            "stat": "goals",
            "min_value": 1,
        },
        "top_assist": {
            "icon": "🎯",
            "title": "Assist King",
            "description": "Người hùng thầm lặng - Chuyên gia dọn cỗ",
            "stat": "assists",
            "min_value": 1,
        },
        "most_appearances": {
            "icon": "🦸",
            "title": "Mr. Reliable",
            "description": "Không nghỉ, không mệt, không biết lười",
            "stat": "matches_played",
            "min_value": 1,
        },
        "top_clean_sheets": {
            "icon": "🧱",
            "title": "Thủ Thành Bất Bại",
            "description": "Bức tường thép - Bóng vào là điều không thể",
            "stat": "clean_sheets",
            "min_value": 1,
        },
        "top_contribution": {
            "icon": "💪",
            "title": "Đóng Góp Số 1",
            "description": "Vừa ghi vừa kiến tạo - Gánh team chuyên nghiệp",
            "stat": "contribution",
            "min_value": 1,
        },
        "best_efficiency": {
            "icon": "⚡",
            "title": "Hiệu Suất Khủng",
            "description": "Ít đá nhưng chất - Ra sân là có bàn",
            "stat": "goal_ratio",
            "min_value": 0.3,
            "min_matches": 5,
        },
    }

    # Danh hiệu tai tiếng
    SHAME_AWARDS = {
        "most_red_cards": {
            "icon": "🃏",
            "title": "Vua Thẻ Đỏ",
            "description": "Võ sĩ đội lốt cầu thủ - Chuyên gia tắm sớm",
            "stat": "red_cards",
            "min_value": 1,
        },
        "most_yellow_cards": {
            "icon": "🟨",
            "title": "Đá Bóng Bẩn Nhất",
            "description": "Chuyên gia phạm lỗi - Đối thủ nhìn là sợ",
            "stat": "yellow_cards",
            "min_value": 3,
        },
        "wooden_leg": {
            "icon": "🦶",
            "title": "Chân Gỗ Vàng",
            "description": "Siêng năng có thừa, bàn thắng thì không",
            "stat": "matches_played",
            "condition": "many_matches_few_goals",
            "min_matches": 10,
        },
        "most_goals_conceded": {
            "icon": "🧤",
            "title": "Vua Nhặt Bóng",
            "description": "Chuyên gia cúi nhặt - Lưới như không có",
            "stat": "goals_conceded",
            "min_value": 5,
        },
        "most_own_goals": {
            "icon": "🥅",
            "title": "Sát Thủ Lưới Nhà",
            "description": "Ghi bàn không chọn lưới - Đồng đội mếu máo",
            "stat": "own_goals",
            "min_value": 1,
        },
    }

    @classmethod
    def get_player_awards(cls, season=None):
        """Lấy danh hiệu cầu thủ"""
        all_stats = PlayerStatsService.get_all_players_stats(season)
        awards = {"glory": [], "shame": []}

        # Glory awards
        for award_key, award_config in cls.GLORY_AWARDS.items():
            stat_key = award_config["stat"]
            min_value = award_config.get("min_value", 0)
            min_matches = award_config.get("min_matches", 0)

            candidates = [
                s for s in all_stats
                if s[stat_key] >= min_value and s["matches_played"] >= min_matches
            ]

            if candidates:
                winner = max(candidates, key=lambda x: x[stat_key])
                awards["glory"].append({
                    "key": award_key,
                    "icon": award_config["icon"],
                    "title": award_config["title"],
                    "description": award_config["description"],
                    "player": winner["player"],
                    "value": winner[stat_key],
                    "stat": stat_key,
                })

        # Shame awards
        for award_key, award_config in cls.SHAME_AWARDS.items():
            stat_key = award_config["stat"]
            min_value = award_config.get("min_value", 0)

            if award_config.get("condition") == "many_matches_few_goals":
                min_matches = award_config.get("min_matches", 10)
                candidates = [
                    s for s in all_stats
                    if s["matches_played"] >= min_matches and s["goals"] <= 2
                ]
                if candidates:
                    winner = max(candidates, key=lambda x: x["matches_played"])
                    awards["shame"].append({
                        "key": award_key,
                        "icon": award_config["icon"],
                        "title": award_config["title"],
                        "description": award_config["description"],
                        "player": winner["player"],
                        "value": winner["matches_played"],
                        "stat": "matches_played",
                    })
            else:
                candidates = [s for s in all_stats if s[stat_key] >= min_value]
                if candidates:
                    winner = max(candidates, key=lambda x: x[stat_key])
                    awards["shame"].append({
                        "key": award_key,
                        "icon": award_config["icon"],
                        "title": award_config["title"],
                        "description": award_config["description"],
                        "player": winner["player"],
                        "value": winner[stat_key],
                        "stat": stat_key,
                    })

        return awards

    @classmethod
    def get_team_awards(cls, season):
        """Lấy danh hiệu đội bóng (League)"""
        if season.type != "LEAGUE":
            return []

        standings = Standing.objects.filter(season=season).order_by("-points", "-goal_diff")
        if not standings.exists():
            return []

        awards = []
        standings_list = list(standings)

        # Champion
        awards.append({
            "icon": "🏆",
            "title": "Nhà Vô Địch",
            "description": "Vua của các vua!",
            "team": standings_list[0].team,
            "value": standings_list[0].points,
        })

        # Runner-up
        if len(standings_list) > 1:
            awards.append({
                "icon": "🥈",
                "title": "Á Quân Đáng Tiếc",
                "description": "Suýt chút nữa thôi...",
                "team": standings_list[1].team,
                "value": standings_list[1].points,
            })

        # Wooden spoon (last place)
        if len(standings_list) > 2:
            awards.append({
                "icon": "🥄",
                "title": "Muỗng Gỗ",
                "description": "Năm sau cố gắng nhé!",
                "team": standings_list[-1].team,
                "value": standings_list[-1].points,
            })

        # Most goals scored
        top_attack = max(standings_list, key=lambda x: x.goals_for)
        awards.append({
            "icon": "⚔️",
            "title": "Cỗ Máy Ghi Bàn",
            "description": "Tấn công là lẽ sống!",
            "team": top_attack.team,
            "value": top_attack.goals_for,
        })

        # Most goals conceded
        worst_defense = max(standings_list, key=lambda x: x.goals_against)
        awards.append({
            "icon": "🕳️",
            "title": "Hàng Thủ Tuyệt Vọng",
            "description": "Phòng ngự là gì?",
            "team": worst_defense.team,
            "value": worst_defense.goals_against,
        })

        return awards


class OverviewService:
    """Service cho trang Overview"""

    @staticmethod
    def get_overview_stats():
        """Lấy thống kê tổng quan"""
        total_players = Player.objects.filter(is_active=True).count()
        total_matches = Match.objects.count()
        total_goals = Goal.objects.exclude(goal_type="OWN_GOAL").count()
        total_cards = Card.objects.count()
        yellow_cards = Card.objects.filter(card_type="YELLOW").count()
        red_cards = Card.objects.filter(card_type="RED").count()

        return {
            "total_players": total_players,
            "total_matches": total_matches,
            "total_goals": total_goals,
            "total_cards": total_cards,
            "yellow_cards": yellow_cards,
            "red_cards": red_cards,
        }

    @staticmethod
    def get_current_season():
        """Lấy mùa giải hiện tại"""
        return Season.objects.filter(is_active=True).first()

    @staticmethod
    def get_top_scorers(limit=10, season=None):
        """Top ghi bàn"""
        goals_filter = Q()
        if season:
            goals_filter = Q(goals__match__season=season)
        
        players = Player.objects.filter(is_active=True).annotate(
            goal_count=Count("goals", filter=goals_filter & ~Q(goals__goal_type="OWN_GOAL"))
        ).filter(goal_count__gt=0).order_by("-goal_count")[:limit]
        
        return [{"player": p, "goals": p.goal_count} for p in players]

    @staticmethod
    def get_top_assists(limit=10, season=None):
        """Top kiến tạo"""
        assists_filter = Q()
        if season:
            assists_filter = Q(assists__match__season=season)
        
        players = Player.objects.filter(is_active=True).annotate(
            assist_count=Count("assists", filter=assists_filter)
        ).filter(assist_count__gt=0).order_by("-assist_count")[:limit]
        
        return [{"player": p, "assists": p.assist_count} for p in players]

    @staticmethod
    def get_top_cards(limit=10, season=None):
        """Top thẻ phạt"""
        cards_filter = Q()
        if season:
            cards_filter = Q(cards__match__season=season)
        
        players = Player.objects.filter(is_active=True).annotate(
            yellow_count=Count("cards", filter=cards_filter & Q(cards__card_type="YELLOW")),
            red_count=Count("cards", filter=cards_filter & Q(cards__card_type="RED")),
            total_cards=Count("cards", filter=cards_filter)
        ).filter(total_cards__gt=0).order_by("-total_cards")[:limit]
        
        return [{
            "player": p,
            "yellow": p.yellow_count,
            "red": p.red_count,
            "total": p.total_cards
        } for p in players]

    @staticmethod
    def get_recent_matches(limit=5):
        """Các trận gần đây"""
        return Match.objects.select_related("season", "home_team", "away_team").prefetch_related("goals", "cards")[:limit]


class SeasonStatsService:
    """Service thống kê chi tiết cho từng mùa giải"""

    @staticmethod
    def get_season_stats(season):
        """Lấy thống kê đầy đủ của một mùa giải"""
        matches = Match.objects.filter(season=season)
        goals = Goal.objects.filter(match__season=season)
        cards = Card.objects.filter(match__season=season)
        
        # Thống kê cơ bản
        total_matches = matches.count()
        total_goals = goals.exclude(goal_type="OWN_GOAL").count()
        total_own_goals = goals.filter(goal_type="OWN_GOAL").count()
        total_cards = cards.count()
        yellow_cards = cards.filter(card_type="YELLOW").count()
        red_cards = cards.filter(card_type="RED").count()
        
        # Tổng số VĐV tham gia (đã ghi bàn, kiến tạo, nhận thẻ hoặc có match_stat)
        player_ids = set()
        player_ids.update(goals.values_list('player_id', flat=True))
        player_ids.update(goals.exclude(assist_by__isnull=True).values_list('assist_by_id', flat=True))
        player_ids.update(cards.values_list('player_id', flat=True))
        player_ids.update(PlayerMatchStat.objects.filter(match__season=season).values_list('player_id', flat=True))
        total_players = len(player_ids)
        
        # TB bàn/trận
        avg_goals_per_match = round(total_goals / total_matches, 2) if total_matches > 0 else 0
        
        # Trận nhiều bàn nhất
        best_match = None
        best_match_goals = 0
        for match in matches:
            match_goals = match.goals.exclude(goal_type="OWN_GOAL").count()
            if match_goals > best_match_goals:
                best_match_goals = match_goals
                best_match = match
        
        # Trận nhiều thẻ nhất
        worst_match = None
        worst_match_cards = 0
        for match in matches:
            match_cards = match.cards.count()
            if match_cards > worst_match_cards:
                worst_match_cards = match_cards
                worst_match = match
        
        # Đếm cú đúp, hat-trick, poker
        braces = 0  # 2 bàn
        hat_tricks = 0  # 3 bàn
        pokers = 0  # 4+ bàn
        
        for match in matches:
            goals_by_player = {}
            for goal in match.goals.exclude(goal_type="OWN_GOAL"):
                pid = str(goal.player_id)
                goals_by_player[pid] = goals_by_player.get(pid, 0) + 1
            
            for count in goals_by_player.values():
                if count >= 4:
                    pokers += 1
                elif count == 3:
                    hat_tricks += 1
                elif count == 2:
                    braces += 1
        
        # Đội nhiều bàn nhất & nhiều thẻ nhất (cho League)
        team_most_goals = None
        team_most_goals_count = 0
        team_most_cards = None
        team_most_cards_count = 0
        
        if season.type == "LEAGUE":
            standings = Standing.objects.filter(season=season)
            for standing in standings:
                if standing.goals_for > team_most_goals_count:
                    team_most_goals_count = standing.goals_for
                    team_most_goals = standing.team
            
            # Đếm thẻ theo đội
            teams = Team.objects.filter(season=season)
            for team in teams:
                team_players = team.players.values_list('player_id', flat=True)
                team_cards = cards.filter(player_id__in=team_players).count()
                if team_cards > team_most_cards_count:
                    team_most_cards_count = team_cards
                    team_most_cards = team
        
        return {
            "season": season,
            "total_players": total_players,
            "total_matches": total_matches,
            "total_goals": total_goals,
            "total_own_goals": total_own_goals,
            "total_cards": total_cards,
            "yellow_cards": yellow_cards,
            "red_cards": red_cards,
            "avg_goals_per_match": avg_goals_per_match,
            "braces": braces,
            "hat_tricks": hat_tricks,
            "pokers": pokers,
            "best_match": best_match,
            "best_match_goals": best_match_goals,
            "worst_match": worst_match,
            "worst_match_cards": worst_match_cards,
            "team_most_goals": team_most_goals,
            "team_most_goals_count": team_most_goals_count,
            "team_most_cards": team_most_cards,
            "team_most_cards_count": team_most_cards_count,
        }

    @staticmethod
    def get_season_top_scorers(season, limit=10):
        """Top ghi bàn trong mùa"""
        return OverviewService.get_top_scorers(limit, season)

    @staticmethod
    def get_season_top_assists(season, limit=10):
        """Top kiến tạo trong mùa"""
        return OverviewService.get_top_assists(limit, season)

    @staticmethod
    def get_season_top_cards(season, limit=10):
        """Top thẻ phạt trong mùa"""
        return OverviewService.get_top_cards(limit, season)

