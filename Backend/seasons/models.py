import uuid
from django.db import models


class Season(models.Model):
    """Mùa giải"""

    class SeasonType(models.TextChoices):
        WEEKLY = "WEEKLY", "Đá Quanh Năm"
        LEAGUE = "LEAGUE", "Đá Giải"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Tên giải", max_length=100)
    type = models.CharField(
        "Loại", 
        max_length=10, 
        choices=SeasonType.choices, 
        default=SeasonType.WEEKLY
    )
    start_date = models.DateField("Ngày bắt đầu", blank=True, null=True)
    end_date = models.DateField("Ngày kết thúc", blank=True, null=True)
    is_active = models.BooleanField("Đang diễn ra", default=False)
    description = models.TextField("Mô tả", blank=True, null=True)

    class Meta:
        verbose_name = "Mùa giải"
        verbose_name_plural = "Mùa giải"
        ordering = ["-start_date", "-is_active"]

    def __str__(self):
        type_label = "🗓️" if self.type == self.SeasonType.WEEKLY else "🏆"
        return f"{type_label} {self.name}"
