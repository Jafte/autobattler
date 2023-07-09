from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import UserFactory
from persons.models import UserPerson
from persons.utils import generate_random_name


class FactoryPage(TemplateView, LoginRequiredMixin):
    template_name = "factories/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            factory = UserFactory.objects.get(user=self.request.user)
        except UserFactory.DoesNotExist:
            factory = UserFactory(
                user=self.request.user
            )
            factory.save()
        except UserFactory.MultipleObjectsReturned:
            factory = UserFactory.objects.filter(user=self.request.user).last()
            UserFactory.objects.exclude(pk=factory.pk).delete()

        context["factory"] = factory
        return context

    def post(self, request, *args, **kwargs):
        person = UserPerson(
            name=generate_random_name(),
            user=self.request.user,
        )
        person.save()
        return redirect("persons-detail", pk=person.pk)
