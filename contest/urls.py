from django.urls import path
from .views import register_user, process_qr, user_dashboard, RealTimeRankingView, rankingView

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("scan/", process_qr, name="process_qr"),
    path("", user_dashboard, name="user_dashboard"),
    path("top/", rankingView, name="top"),
    path('api/ranking/', RealTimeRankingView.as_view(), name='real-time-ranking'),
]
