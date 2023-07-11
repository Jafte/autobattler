from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import Http404
from persons.enums import PersonStatus
from persons.models import UserPerson
from raids.models import UserRaid
from raids.enums import RaidStatus
from gameplay.raid.standard import GameplayRaid


class RaidListPage(LoginRequiredMixin, TemplateView):
    template_name = "raids/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_raids"] = UserRaid.objects.filter(status=RaidStatus.NEW)
        context["finished_raids"] = UserRaid.objects.filter(status=RaidStatus.FINISHED)
        return context


class RaidSessionPage(LoginRequiredMixin, TemplateView):
    template_name = "raids/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["raid"] = UserRaid.objects.get(pk=kwargs["pk"])
        except UserRaid.DoesNotExist:
            raise Http404("Raid does not exist")
        return context


class RaidSessionJoinPage(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        person_pk = request.POST.get('person_pk')
        try:
            person = UserPerson.objects.get(pk=person_pk, user=self.request.user, status=PersonStatus.ALIVE)
        except UserPerson.DoesNotExist:
            raise Http404("Person does not exist")

        try:
            raid = UserRaid.objects.get(pk=kwargs["pk"], status=RaidStatus.NEW)
        except UserRaid.DoesNotExist:
            raise Http404("Raid does not exist")

        person.raid_session = raid
        person.save()

        return redirect("raids-detail", pk=raid.pk)


class RaidSessionStartPage(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            user_raid = UserRaid.objects.get(pk=kwargs["pk"], status=RaidStatus.NEW)
        except UserRaid.DoesNotExist:
            raise Http404("Raid does not exist")

        user_raid.status = RaidStatus.IN_PROGRESS
        user_raid.save()

        game = GameplayRaid.create_from_user_raid(user_raid)
        game.start()
        game.play()

        user_raid.update_from_raid(game)

        return redirect("raids-detail", pk=user_raid.pk)
