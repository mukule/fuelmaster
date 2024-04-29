
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('main/', include('main.urls', namespace='main')),
    path('company/', include('company.urls', namespace='company')),
    path('inventory/', include('inventory.urls', namespace='inventory')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
