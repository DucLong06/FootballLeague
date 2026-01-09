import uuid
from django.db import models
from seasons.models import Season
from players.models import Player


class Team(models.Model):
    """Đội bóng - Chỉ dùng cho LEAGUE"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(
        Season, 
        on_delete=models.CASCADE, 
        related_name="teams",
        verbose_name="Thuộc giải"
    )
    name = models.CharField("Tên đội", max_length=100)
    logo = models.ImageField("Logo đội", upload_to="team_logos/", blank=True, null=True)
    color = models.CharField("Màu áo", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Đội bóng"
        verbose_name_plural = "Đội bóng"
        ordering = ["name"]
        unique_together = ["season", "name"]

    def __str__(self):
        return f"{self.name} ({self.season.name})"


class TeamPlayer(models.Model):
    """Cầu thủ thuộc đội - Chỉ dùng cho LEAGUE"""

    class Position(models.TextChoices):
        GK = "GK", "Thủ môn"
        DF = "DF", "Hậu vệ"
        MF = "MF", "Tiền vệ"
        FW = "FW", "Tiền đạo"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        related_name="players",
        verbose_name="Đội"
    )
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE, 
        related_name="team_assignments",
        verbose_name="Cầu thủ"
    )
    jersey_number = models.PositiveSmallIntegerField("Số áo", blank=True, null=True)
    position = models.CharField(
        "Vị trí", 
        max_length=2, 
        choices=Position.choices, 
        blank=True, 
        null=True
    )
    is_captain = models.BooleanField("Đội trưởng", default=False)

    class Meta:
        verbose_name = "Cầu thủ trong đội"
        verbose_name_plural = "Cầu thủ trong đội"
        unique_together = ["team", "player"]

    def __str__(self):
        captain = " (C)" if self.is_captain else ""
        number = f" #{self.jersey_number}" if self.jersey_number else ""
        return f"{self.player.name}{number}{captain}"
