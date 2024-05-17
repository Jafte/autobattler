import jwt
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, FormView

from gameplay.raid.base import BaseRaid
from raids.enums import RaidStatus
from raids.models import Raid
from robots.enums import RobotAction, RobotStatus
from robots.forms import RobotActionForm, RobotCreatForm
from robots.models import Robot


class RobotListView(LoginRequiredMixin, ListView):
    context_object_name = "robot_list"
    template_name = "infra/robot_list.html"
    paginate_by = 20

    def get_queryset(self):
        return Robot.objects.filter(user=self.request.user).order_by("-created_at")


class RobotDetailView(LoginRequiredMixin, DetailView, FormView):
    form_class = RobotActionForm
    context_object_name = "robot"
    template_name = "infra/robot_detail.html"

    def get_queryset(self):
        return Robot.objects.filter(user=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_raids"] = self.object.raid_robots.prefetch_related("raid").order_by("-raid__created_at")[:5]
        return context

    def form_valid(self, form):
        self.object = self.get_object()
        action = form.cleaned_data["action"]
        if action == RobotAction.SEND_TO_RAID:
            # self.object.status = RobotStatus.PREPARATION
            self.object.status = RobotStatus.ON_MISSION
            self.object.save()
            game = BaseRaid.create_for_user(self.object)
            raid = Raid(status=RaidStatus.IN_PROGRESS)
            raid.save_gameplay_to_model(gameplay_raid=game)
        if action == RobotAction.DISASSEMBLE:
            self.object.status = RobotStatus.DEAD
            self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class RobotCreateView(LoginRequiredMixin, FormView):
    form_class = RobotCreatForm
    template_name = "infra/robot_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.robot_options:
            self.request.user.generate_new_robot_options()
        context["robot_options"] = self.request.user.robot_options
        active_robots_num = Robot.objects.filter(user=self.request.user).exclude(status=RobotStatus.DEAD).count()
        active_robots_max = self.request.user.get_max_robots()
        context["can_create_robots"] = active_robots_num < active_robots_max
        return context

    def form_valid(self, form):
        key = settings.SECRET_KEY
        robot_option = jwt.decode(form.cleaned_data["robot_option_key"], key, algorithms="HS256")
        self.object = Robot(
            user=self.request.user,
            name=form.cleaned_data["name"],
            strength=robot_option["strength"],
            dexterity=robot_option["dexterity"],
            intelligence=robot_option["intelligence"],
            constitution=robot_option["constitution"],
            wisdom=robot_option["wisdom"],
            charisma=robot_option["charisma"],
        )
        self.object.save()
        self.request.user.generate_new_robot_options()
        return HttpResponseRedirect(self.object.get_absolute_url())
