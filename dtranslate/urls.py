from django.contrib import admin
from django.urls import path, include

from items.views import create

urlpatterns = [
    path('', create, name='index'),
    path('admin/', admin.site.urls),
    path('projects', include('projects.urls')),
]
