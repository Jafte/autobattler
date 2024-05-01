from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.views.generic.base import TemplateView

from robots.models import Robot
from raids.models import Raid


class IndexView(TemplateView):
    template_name = "index.html"


class InfraDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "infra/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["robots"] = Robot.objects.filter(user=self.request.user).order_by("-created_at")[:10]
        user_robots = Count('robots', Q(robots__user=self.request.user))
        context["raids"] = Raid.objects.annotate(num_user_robots=user_robots).filter(num_user_robots__gt=0).order_by("-created_at")[:10]
        return context
