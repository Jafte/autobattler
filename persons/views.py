from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import Http404
from persons.models import UserPerson
from persons.enums import PersonStatus
from persons.utils import generate_random_name
from raids.enums import RaidStatus
from raids.models import UserRaid


class PersonsListPage(TemplateView, LoginRequiredMixin):
    template_name = "persons/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alive_persons"] = UserPerson.objects.filter(user=self.request.user, status=PersonStatus.ALIVE)
        context["dead_persons"] = UserPerson.objects.filter(user=self.request.user, status=PersonStatus.DEAD)
        return context


class PersonPage(TemplateView, LoginRequiredMixin):
    template_name = "persons/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["person"] = UserPerson.objects.get(pk=kwargs["pk"], user=self.request.user)
        except UserPerson.DoesNotExist:
            raise Http404("Dall does not exist")
        context["raids"] = UserRaid.objects.filter(status=RaidStatus.NEW)
        return context


class PersonCreatePage(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        person = UserPerson(
            name=generate_random_name(),
            user=self.request.user,
        )
        person.save()
        return redirect("persons-detail", pk=person.pk)
