from django.contrib import admin
from django.urls import path, include

from videos.views import create

urlpatterns = [
    path('', create),
    path('admin/', admin.site.urls),
    path('videos/', include('videos.urls'))
]
