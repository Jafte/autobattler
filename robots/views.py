from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, FormView

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
            self.object.status = RobotStatus.PREPARATION
            self.object.save()
        if action == RobotAction.DISASSEMBLE:
            self.object.status = RobotStatus.DEAD
            self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class RobotCreateView(LoginRequiredMixin, CreateView):
    model = Robot
    form_class = RobotCreatForm
    template_name = "infra/robot_add.html"

    def form_valid(self, form):
        self.object = Robot(
            user=self.request.user,
            name=form.cleaned_data["name"],
            strength=form.cleaned_data["strength"],
            agility=form.cleaned_data["agility"],
        )
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
