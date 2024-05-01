from django.urls import path

from robots.views import RobotDetailView, RobotListView, RobotCreateView

urlpatterns = [
    path("", RobotListView.as_view(), name="infra_robot_list"),
    path("add/", RobotCreateView.as_view(), name="infra_robot_add"),
    path("<pk>/", RobotDetailView.as_view(), name="infra_robot_detail"),
]
