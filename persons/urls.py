from django.urls import path
from persons.views import PersonsListPage, PersonPage, PersonCreatePage

urlpatterns = [
    path('', PersonsListPage.as_view(), name='persons-list'),
    path('<int:pk>/', PersonPage.as_view(), name='persons-detail'),
    path('create/', PersonCreatePage.as_view(), name='persons-create'),
]
