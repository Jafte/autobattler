from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.views.generic import DetailView, ListView

from raids.models import Raid

class RaidListView(LoginRequiredMixin, ListView):
    context_object_name = "raid_list"
    template_name = "infra/raid_list.html"
    paginate_by = 30

    def get_queryset(self):
        user_robots = Count('robots', Q(robots__user=self.request.user))
        return Raid.objects.annotate(num_user_robots=user_robots).filter(num_user_robots__gt=0).order_by("-created_at")


class RaidDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "raid"
    template_name = "infra/raid_detail.html"

    def get_queryset(self):
        user_robots = Count('robots', Q(robots__user=self.request.user))
        return Raid.objects.annotate(num_user_robots=user_robots).filter(num_user_robots__gt=0).order_by("-created_at")
