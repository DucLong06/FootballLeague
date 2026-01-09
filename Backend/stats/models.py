import uuid
from django.db import models
from seasons.models import Season
from teams.models import Team


class Standing(models.Model):
    """Bảng xếp hạng - Chỉ dùng cho LEAGUE"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(
        Season, 
        on_delete=models.CASCADE, 
        related_name="standings",
        verbose_name="Giải đấu"
    )
    team = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        related_name="standings",
        verbose_name="Đội"
    )
    played = models.PositiveSmallIntegerField("Số trận", default=0)
    won = models.PositiveSmallIntegerField("Thắng", default=0)
    drawn = models.PositiveSmallIntegerField("Hòa", default=0)
    lost = models.PositiveSmallIntegerField("Thua", default=0)
    goals_for = models.PositiveSmallIntegerField("Bàn thắng", default=0)
    goals_against = models.PositiveSmallIntegerField("Bàn thua", default=0)
    goal_diff = models.SmallIntegerField("Hiệu số", default=0)
    points = models.PositiveSmallIntegerField("Điểm", default=0)

    class Meta:
        verbose_name = "Bảng xếp hạng"
        verbose_name_plural = "Bảng xếp hạng"
        ordering = ["-points", "-goal_diff", "-goals_for"]
        unique_together = ["season", "team"]

    def __str__(self):
        return f"{self.team.name} - {self.points} điểm"

    def update_stats(self):
        """Cập nhật thống kê từ các trận đấu"""
        from matches.models import Match
        
        home_matches = Match.objects.filter(
            home_team=self.team,
            home_score__isnull=False,
            away_score__isnull=False
        )
        away_matches = Match.objects.filter(
            away_team=self.team,
            home_score__isnull=False,
            away_score__isnull=False
        )
        
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.goals_for = 0
        self.goals_against = 0
        
        for match in home_matches:
            self.played += 1
            self.goals_for += match.home_score
            self.goals_against += match.away_score
            if match.home_score > match.away_score:
                self.won += 1
            elif match.home_score == match.away_score:
                self.drawn += 1
            else:
                self.lost += 1
        
        for match in away_matches:
            self.played += 1
            self.goals_for += match.away_score
            self.goals_against += match.home_score
            if match.away_score > match.home_score:
                self.won += 1
            elif match.away_score == match.home_score:
                self.drawn += 1
            else:
                self.lost += 1
        
        self.goal_diff = self.goals_for - self.goals_against
        self.points = self.won * 3 + self.drawn
        self.save()
