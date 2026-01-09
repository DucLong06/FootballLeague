"""
Script tạo sample data cho CSOC Football
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from datetime import datetime, timedelta
from players.models import Player
from seasons.models import Season
from matches.models import Match, Goal, Card, PlayerMatchStat


def create_sample_data():
    print("🚀 Bắt đầu tạo sample data cho CSOC Football...")
    
    # Xóa dữ liệu cũ
    Goal.objects.all().delete()
    Card.objects.all().delete()
    PlayerMatchStat.objects.all().delete()
    Match.objects.all().delete()
    Season.objects.all().delete()
    Player.objects.all().delete()
    
    print("✓ Đã xóa dữ liệu cũ")
    
    # Tạo cầu thủ
    players_data = [
        {"name": "Nguyễn Văn Hùng", "nickname": "Hùng Xồi"},
        {"name": "Trần Minh Đức", "nickname": "Đức Béo"},
        {"name": "Lê Hoàng Nam", "nickname": "Nam Lùn"},
        {"name": "Phạm Quốc Bảo", "nickname": "Bảo Đen"},
        {"name": "Võ Thanh Tùng", "nickname": "Tùng Mập"},
        {"name": "Hoàng Văn Long", "nickname": "Long Đầu Bạc"},
        {"name": "Đặng Minh Tuấn", "nickname": "Tuấn Thủ Môn"},
        {"name": "Bùi Xuân Trường", "nickname": "Trường Sói"},
        {"name": "Ngô Đình Phong", "nickname": "Phong Già"},
        {"name": "Lý Quang Hải", "nickname": "Hải Messi"},
        {"name": "Trịnh Văn Quyết", "nickname": "Quyết Tóc Dài"},
        {"name": "Mai Xuân Hợp", "nickname": "Hợp Ronaldo"},
        {"name": "Đinh Công Thành", "nickname": "Thành Cao"},
        {"name": "Vũ Đức Anh", "nickname": "Anh Phê"},
        {"name": "Phan Văn Toàn", "nickname": "Toàn Chân Gỗ"},
    ]
    
    players = []
    for data in players_data:
        player = Player.objects.create(**data)
        players.append(player)
    
    print(f"✓ Đã tạo {len(players)} cầu thủ")
    
    # Tạo mùa giải Weekly 2025
    season = Season.objects.create(
        name="Weekly 2025",
        type="WEEKLY",
        start_date=datetime(2025, 1, 1),
        is_active=True,
        description="Đá phong trào hàng tuần năm 2025"
    )
    print(f"✓ Đã tạo mùa giải: {season.name}")
    
    # Tạo các trận đấu
    match_dates = [
        datetime(2025, 1, 2, 19, 0),
        datetime(2025, 1, 9, 19, 0),
        datetime(2025, 1, 16, 19, 0),
        datetime(2025, 1, 23, 19, 0),
        datetime(2025, 1, 30, 19, 0),
        datetime(2025, 2, 6, 19, 0),
        datetime(2025, 2, 13, 19, 0),
        datetime(2025, 2, 20, 19, 0),
    ]
    
    matches = []
    for i, date in enumerate(match_dates):
        match = Match.objects.create(
            season=season,
            match_date=date,
            venue="Sân bóng CSOC",
            notes=f"Trận thứ {i+1} - Weekly 2025"
        )
        matches.append(match)
    
    print(f"✓ Đã tạo {len(matches)} trận đấu")
    
    # Thêm bàn thắng và kiến tạo
    import random
    
    goals_data = [
        # Trận 1
        (0, 0, 1, 15, "NORMAL"),  # Nguyễn Văn Hùng ghi, Trần Minh Đức kiến tạo
        (0, 9, 2, 32, "HEADER"),  # Lý Quang Hải ghi, Lê Hoàng Nam kiến tạo
        (0, 11, None, 67, "FREE_KICK"),  # Mai Xuân Hợp đá phạt
        # Trận 2
        (1, 0, 3, 12, "NORMAL"),
        (1, 0, 9, 45, "NORMAL"),
        (1, 3, 0, 78, "HEADER"),
        (1, 9, 11, 89, "PENALTY"),
        # Trận 3
        (2, 11, 9, 23, "NORMAL"),
        (2, 0, 2, 56, "NORMAL"),
        (2, 9, 0, 71, "NORMAL"),
        (2, 2, 11, 85, "HEADER"),
        # Trận 4
        (3, 3, 0, 10, "NORMAL"),
        (3, 0, 3, 34, "NORMAL"),
        (3, 11, None, 55, "FREE_KICK"),
        (3, 9, 0, 78, "PENALTY"),
        (3, 0, 9, 90, "NORMAL"),
        # Trận 5
        (4, 0, 11, 15, "NORMAL"),
        (4, 9, 3, 28, "HEADER"),
        (4, 11, 0, 45, "NORMAL"),
        (4, 3, 9, 62, "NORMAL"),
        (4, 0, 2, 88, "NORMAL"),
        # Trận 6
        (5, 9, 0, 5, "NORMAL"),
        (5, 0, 9, 33, "NORMAL"),
        (5, 11, 3, 67, "HEADER"),
        # Trận 7
        (6, 0, 11, 22, "NORMAL"),
        (6, 9, None, 45, "PENALTY"),
        (6, 3, 0, 55, "NORMAL"),
        (6, 0, 3, 78, "NORMAL"),
        (6, 11, 9, 85, "HEADER"),
        # Trận 8
        (7, 0, 9, 8, "NORMAL"),
        (7, 9, 0, 25, "NORMAL"),
        (7, 11, 3, 42, "FREE_KICK"),
        (7, 0, 2, 66, "NORMAL"),
        (7, 3, 11, 88, "HEADER"),
        # Phản lưới
        (3, 14, None, 65, "OWN_GOAL"),  # Toàn Chân Gỗ phản lưới
    ]
    
    goal_count = 0
    for match_idx, scorer_idx, assist_idx, minute, goal_type in goals_data:
        Goal.objects.create(
            match=matches[match_idx],
            player=players[scorer_idx],
            assist_by=players[assist_idx] if assist_idx is not None else None,
            minute=minute,
            goal_type=goal_type
        )
        goal_count += 1
    
    print(f"✓ Đã tạo {goal_count} bàn thắng")
    
    # Thêm thẻ phạt
    cards_data = [
        (0, 4, "YELLOW", 25, "Phạm lỗi thô bạo"),
        (1, 7, "YELLOW", 55, "Câu giờ"),
        (1, 4, "YELLOW", 78, "Phản ứng với trọng tài"),
        (2, 5, "YELLOW", 34, "Kéo áo"),
        (2, 4, "YELLOW", 67, "Vào bóng nguy hiểm"),
        (2, 4, "RED", 68, "2 thẻ vàng"),
        (3, 7, "YELLOW", 45, "Phạm lỗi chiến thuật"),
        (4, 5, "YELLOW", 22, "Cản phá phản công"),
        (4, 7, "YELLOW", 56, "Chơi xấu"),
        (5, 4, "YELLOW", 33, "Đá người"),
        (5, 13, "YELLOW", 78, "Mất bình tĩnh"),
        (6, 5, "YELLOW", 44, "Phạm lỗi vùng cấm"),
        (7, 7, "YELLOW", 25, "Vào bóng quyết liệt"),
        (7, 4, "RED", 85, "Bạo lực"),
    ]
    
    card_count = 0
    for match_idx, player_idx, card_type, minute, reason in cards_data:
        Card.objects.create(
            match=matches[match_idx],
            player=players[player_idx],
            card_type=card_type,
            minute=minute,
            reason=reason
        )
        card_count += 1
    
    print(f"✓ Đã tạo {card_count} thẻ phạt")
    
    # Thêm player match stats (ra sân)
    stats_count = 0
    for match in matches:
        # Mỗi trận có ~10-12 người ra sân
        participating = random.sample(players, random.randint(10, 12))
        for i, player in enumerate(participating):
            PlayerMatchStat.objects.create(
                match=match,
                player=player,
                is_starter=(i < 7),
                minutes_played=random.randint(45, 90),
                is_goalkeeper=(player.nickname == "Tuấn Thủ Môn"),
                clean_sheet=False,
                goals_conceded=random.randint(0, 2) if player.nickname == "Tuấn Thủ Môn" else None,
                saves=random.randint(3, 8) if player.nickname == "Tuấn Thủ Môn" else None
            )
            stats_count += 1
    
    print(f"✓ Đã tạo {stats_count} thống kê ra sân")
    
    print("\n" + "="*50)
    print("🎉 HOÀN THÀNH TẠO SAMPLE DATA CHO CSOC FOOTBALL!")
    print("="*50)
    print(f"📊 Tổng kết:")
    print(f"   - {len(players)} cầu thủ")
    print(f"   - 1 mùa giải (Weekly 2025)")
    print(f"   - {len(matches)} trận đấu")
    print(f"   - {goal_count} bàn thắng")
    print(f"   - {card_count} thẻ phạt")
    print(f"   - {stats_count} thống kê ra sân")
    print("\n➡️ Truy cập http://localhost:5173/ để xem kết quả!")


if __name__ == "__main__":
    create_sample_data()
