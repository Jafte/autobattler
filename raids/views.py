from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import Http404
from persons.enums import PersonStatus
from persons.models import UserPerson
from raids.models import RaidSession
from raids.enums import RaidStatus
from raids.raid import Raid as Game


class RaidRulesListPage(TemplateView, LoginRequiredMixin):
    template_name = "raids/rules.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_raids"] = RaidSession.objects.filter(status=RaidStatus.NEW)
        context["finished_raids"] = RaidSession.objects.filter(status=RaidStatus.FINISHED)
        return context


class RaidSessionPage(TemplateView, LoginRequiredMixin):
    template_name = "raids/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["raid"] = RaidSession.objects.get(pk=kwargs["pk"])
        except RaidSession.DoesNotExist:
            raise Http404("Raid does not exist")
        return context


class RaidSessionJoinPage(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        person_pk = request.POST.get('person_pk')
        try:
            person = UserPerson.objects.get(pk=person_pk, user=self.request.user, status=PersonStatus.ALIVE)
        except UserPerson.DoesNotExist:
            raise Http404("Person does not exist")

        try:
            raid = RaidSession.objects.get(pk=kwargs["pk"], status=RaidStatus.NEW)
        except RaidSession.DoesNotExist:
            raise Http404("Raid does not exist")

        person.raid_session = raid
        person.save()

        return redirect("raids-detail", pk=raid.pk)


class RaidSessionStartPage(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        try:
            raid = RaidSession.objects.get(pk=kwargs["pk"], status=RaidStatus.NEW)
        except RaidSession.DoesNotExist:
            raise Http404("Raid does not exist")

        raid.status = RaidStatus.IN_PROGRESS
        raid.save()

        game = Game.create_from_session(raid)
        game.start()
        game.play()

        raid.update_from_raid(game)

        return redirect("raids-detail", pk=raid.pk)
