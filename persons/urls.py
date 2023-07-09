from django.urls import path
from persons.views import PersonsListPage, PersonPage

urlpatterns = [
    path('', PersonsListPage.as_view(), name='persons-list'),
    path('<int:pk>/', PersonPage.as_view(), name='persons-detail'),
]
