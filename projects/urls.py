from django.urls import path

from .views import ProjectListView
from .views import ProjectDetailView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('<int:pk>', ProjectDetailView.as_view(), name='detail'),
]
