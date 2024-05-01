from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, FormView

from robots.enums import RobotAction, RobotStatus
from robots.forms import RobotActionForm
from robots.models import Robot


class RobotListView(LoginRequiredMixin, ListView):
    context_object_name = "robot_list"
    template_name = "infra/robot_list.html"

    def get_queryset(self):
        return Robot.objects.filter(user=self.request.user).order_by("-created_at")


class RobotDetailView(LoginRequiredMixin, DetailView, FormView):
    form_class = RobotActionForm
    context_object_name = "robot"
    template_name = "infra/robot_detail.html"

    def get_queryset(self):
        return Robot.objects.filter(user=self.request.user).order_by("-created_at")

    def form_valid(self, form):
        self.object = self.get_object()
        action = form.cleaned_data["action"]
        if action == RobotAction.SEND_TO_RAID:
            self.object.status = RobotStatus.ON_MISSION
            self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class RobotCreateView(LoginRequiredMixin, CreateView):
    model = Robot
    fields = ["name"]
    template_name = "infra/robot_add.html"

    def form_valid(self, form):
        self.object = Robot(
            user=self.request.user,
            name=form.cleaned_data["name"],
            max_health=100,
        )
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
