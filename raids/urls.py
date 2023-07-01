from django.urls import path
from raids.views import RaidRulesListPage, RaidSessionPage, RaidSessionJoinPage, RaidSessionStartPage

urlpatterns = [
    path('', RaidRulesListPage.as_view(), name='raids-rules'),
    path('<int:pk>/', RaidSessionPage.as_view(), name='raids-detail'),
    path('<int:pk>/join', RaidSessionJoinPage.as_view(), name='raids-detail-join'),
    path('<int:pk>/start', RaidSessionStartPage.as_view(), name='raids-detail-start'),
]
