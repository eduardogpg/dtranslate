from django.contrib import admin
from django.urls import path, include

from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('items/', include('items.urls')),
    path('projects/', include('projects.urls')),
]
