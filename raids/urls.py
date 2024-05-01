from django.urls import path

from raids.views import RaidDetailView, RaidListView

urlpatterns = [
    path("", RaidListView.as_view(), name="infra_raid_list"),
    path("<pk>/", RaidDetailView.as_view(), name="infra_raid_detail"),
]
