from django.urls import path
from . import views


app_name = 'main'
urlpatterns = [
    path("index/", views.index, name="index"),
    path("branch/", views.branch, name="branch"),
]
