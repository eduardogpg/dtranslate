from django.urls import path

from .views import create, detail, delete, download

app_name = 'items'

urlpatterns = [
    path('', create, name='create'),
    path('<int:pk>', detail, name='detail'),
    path('delete/<int:pk>', delete, name='delete'),
    path('download/<int:pk>', download, name='download'),
]
