from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OverviewAPIView,
    PlayerViewSet,
    SeasonViewSet,
    TeamViewSet,
    MatchViewSet,
    StandingViewSet,
    AwardsAPIView,
)

router = DefaultRouter()
router.register(r"players", PlayerViewSet)
router.register(r"seasons", SeasonViewSet)
router.register(r"teams", TeamViewSet)
router.register(r"matches", MatchViewSet)
router.register(r"standings", StandingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("overview/", OverviewAPIView.as_view(), name="overview"),
    path("awards/", AwardsAPIView.as_view(), name="awards"),
]
