from django.urls import path
from uis.views import IndexPage


urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
]
