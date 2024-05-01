from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import IndexView, InfraDashboardView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("infra/raid/", include("raids.urls")),
    path("infra/robot/", include("robots.urls")),
    path("infra/", InfraDashboardView.as_view(), name="infra_dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
