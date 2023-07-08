from django.urls import path
from .views import FactoryPage

urlpatterns = [
    path('', FactoryPage.as_view(), name='factory-detail'),
]
