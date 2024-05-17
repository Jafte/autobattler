import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import DetailView, ListView, FormView

from raids.forms import RaidActionForm
from raids.models import Raid


class RaidListView(LoginRequiredMixin, ListView):
    context_object_name = "raid_list"
    template_name = "infra/raid_list.html"
    paginate_by = 20

    def get_queryset(self):
        user_robots = Count('robots', Q(robots__user=self.request.user))
        return Raid.objects.annotate(num_user_robots=user_robots).filter(num_user_robots__gt=0).order_by("-created_at")


class RaidDetailView(LoginRequiredMixin, DetailView):
    form_class = RaidActionForm
    context_object_name = "raid"
    template_name = "infra/raid_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["robots"] = self.object.robots.filter(user=self.request.user)
        context["active_robot_uuid"] = context["robots"][0].uuid
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = json.loads(request.body)
        game = self.object.restore_gameplay_from_model()
        game.move_user(user_uuid=data['uuid'], x=data['x'], y=data['y'])
        self.object.save_gameplay_to_model(gameplay_raid=game)
        return JsonResponse({
            "success": True,
            "is_ended": game.is_ended,
            "config_state": self.object.config_state,
            "bots_state": self.object.bots_state,
            "users_state": self.object.users_state,
        })

    def get_queryset(self):
        user_robots = Count('robots', Q(robots__user=self.request.user))
        return Raid.objects.annotate(num_user_robots=user_robots).filter(num_user_robots__gt=0).order_by("-created_at")
