import uuid
from django.db import models


class Player(models.Model):
    """Cầu thủ"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Họ tên", max_length=100)
    avatar = models.ImageField("Ảnh đại diện", upload_to="avatars/", blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    nickname = models.CharField("Biệt danh", max_length=50, blank=True, null=True)
    is_active = models.BooleanField("Còn tham gia", default=True)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

    class Meta:
        verbose_name = "Cầu thủ"
        verbose_name_plural = "Cầu thủ"
        ordering = ["name"]

    def __str__(self):
        if self.nickname:
            return f"{self.name} ({self.nickname})"
        return self.name
