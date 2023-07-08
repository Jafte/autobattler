from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserFactory


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
