from django.urls import path

from .views import create

app_name = 'items'

urlpatterns = [
    path('', create, name='create'),
]
