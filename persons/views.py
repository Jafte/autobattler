from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from persons.models import UserPerson
from persons.enums import PersonStatus
from raids.enums import RaidStatus
from raids.models import UserRaid


class PersonsListPage(LoginRequiredMixin, TemplateView):
    template_name = "persons/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alive_persons"] = UserPerson.objects.filter(user=self.request.user, status=PersonStatus.ALIVE)
        context["dead_persons"] = UserPerson.objects.filter(user=self.request.user, status=PersonStatus.DEAD).order_by('-id')[:10]
        return context


class PersonPage(LoginRequiredMixin, TemplateView):
    template_name = "persons/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["person"] = UserPerson.objects.get(pk=kwargs["pk"], user=self.request.user)
        except UserPerson.DoesNotExist:
            raise Http404("Dall does not exist")
        context["raids"] = UserRaid.objects.filter(status=RaidStatus.NEW)
        return context
