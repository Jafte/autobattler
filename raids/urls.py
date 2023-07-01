from django.urls import path
from raids.views import RaidListPage, RaidSessionPage, RaidSessionJoinPage, RaidSessionStartPage

urlpatterns = [
    path('', RaidListPage.as_view(), name='raids-list'),
    path('<int:pk>/', RaidSessionPage.as_view(), name='raids-detail'),
    path('<int:pk>/join', RaidSessionJoinPage.as_view(), name='raids-detail-join'),
    path('<int:pk>/start', RaidSessionStartPage.as_view(), name='raids-detail-start'),
]
