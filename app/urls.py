from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('uis.urls')),
    path('factories/', include('factories.urls')),
    path('persons/', include('persons.urls')),
    path('raids/', include('raids.urls')),
    path('accounts/', include('accounts.urls')),

    path('admin/', admin.site.urls),
]
