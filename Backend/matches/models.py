import uuid
from django.db import models
from seasons.models import Season
from teams.models import Team
from players.models import Player


class Match(models.Model):
    """Trận đấu"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(
        Season, 
        on_delete=models.CASCADE, 
        related_name="matches",
        verbose_name="Mùa giải"
    )
    match_date = models.DateTimeField("Ngày giờ", blank=True, null=True)
    venue = models.CharField("Địa điểm", max_length=200, blank=True, null=True)
    round = models.PositiveSmallIntegerField("Vòng đấu", blank=True, null=True)
    
    # Chỉ dùng cho League
    home_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="home_matches",
        verbose_name="Đội nhà",
        blank=True,
        null=True
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="away_matches",
        verbose_name="Đội khách",
        blank=True,
        null=True
    )
    home_score = models.PositiveSmallIntegerField("Tỷ số đội nhà", blank=True, null=True)
    away_score = models.PositiveSmallIntegerField("Tỷ số đội khách", blank=True, null=True)
    notes = models.TextField("Ghi chú", blank=True, null=True)

    class Meta:
        verbose_name = "Trận đấu"
        verbose_name_plural = "Trận đấu"
        ordering = ["-match_date"]

    def __str__(self):
        if self.home_team and self.away_team:
            score = f"{self.home_score or '?'} - {self.away_score or '?'}"
            return f"{self.home_team.name} {score} {self.away_team.name}"
        date_str = self.match_date.strftime("%d/%m/%Y") if self.match_date else "TBD"
        return f"Trận {date_str} ({self.season.name})"


class Goal(models.Model):
    """Bàn thắng"""

    class GoalType(models.TextChoices):
        NORMAL = "NORMAL", "Bình thường"
        PENALTY = "PENALTY", "Penalty"
        FREE_KICK = "FREE_KICK", "Đá phạt"
        HEADER = "HEADER", "Đánh đầu"
        OWN_GOAL = "OWN_GOAL", "Phản lưới"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, 
        on_delete=models.CASCADE, 
        related_name="goals",
        verbose_name="Trận đấu"
    )
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name="goals",
        verbose_name="Người ghi bàn"
    )
    assist_by = models.ForeignKey(
        Player, 
        on_delete=models.SET_NULL, 
        related_name="assists",
        verbose_name="Người kiến tạo",
        blank=True,
        null=True
    )
    minute = models.PositiveSmallIntegerField("Phút ghi bàn", blank=True, null=True)
    goal_type = models.CharField(
        "Loại bàn thắng",
        max_length=15,
        choices=GoalType.choices,
        default=GoalType.NORMAL
    )
    for_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="goals",
        verbose_name="Ghi cho đội",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Bàn thắng"
        verbose_name_plural = "Bàn thắng"
        ordering = ["match", "minute"]

    def __str__(self):
        minute = f"({self.minute}')" if self.minute else ""
        return f"⚽ {self.player.name} {minute}"


class Card(models.Model):
    """Thẻ phạt"""

    class CardType(models.TextChoices):
        YELLOW = "YELLOW", "Thẻ vàng"
        RED = "RED", "Thẻ đỏ"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, 
        on_delete=models.CASCADE, 
        related_name="cards",
        verbose_name="Trận đấu"
    )
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name="cards",
        verbose_name="Cầu thủ"
    )
    card_type = models.CharField(
        "Loại thẻ",
        max_length=10,
        choices=CardType.choices
    )
    minute = models.PositiveSmallIntegerField("Phút nhận thẻ", blank=True, null=True)
    reason = models.CharField("Lý do", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Thẻ phạt"
        verbose_name_plural = "Thẻ phạt"
        ordering = ["match", "minute"]

    def __str__(self):
        icon = "🟨" if self.card_type == self.CardType.YELLOW else "🟥"
        minute = f"({self.minute}')" if self.minute else ""
        return f"{icon} {self.player.name} {minute}"


class PlayerMatchStat(models.Model):
    """Thống kê cầu thủ mỗi trận"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, 
        on_delete=models.CASCADE, 
        related_name="player_stats",
        verbose_name="Trận đấu"
    )
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name="match_stats",
        verbose_name="Cầu thủ"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="player_match_stats",
        verbose_name="Đội",
        blank=True,
        null=True
    )
    is_starter = models.BooleanField("Đá chính", default=True)
    minutes_played = models.PositiveSmallIntegerField("Số phút thi đấu", blank=True, null=True)
    is_goalkeeper = models.BooleanField("Là thủ môn", default=False)
    goals_conceded = models.PositiveSmallIntegerField("Số bàn thua", blank=True, null=True)
    clean_sheet = models.BooleanField("Giữ sạch lưới", default=False)
    saves = models.PositiveSmallIntegerField("Số pha cứu thua", blank=True, null=True)

    class Meta:
        verbose_name = "Thống kê trận đấu"
        verbose_name_plural = "Thống kê trận đấu"
        unique_together = ["match", "player"]

    def __str__(self):
        return f"{self.player.name} - {self.match}"
