from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('', include('account.urls', namespace='account')),
    path('', include('myadmin.urls', namespace='myadmin')),
]
