from django.urls import path
from .views import *

app_name = 'company'
urlpatterns = [
    path('create/', create_company, name='create_company'),
    path('companies/<int:pk>/', company_detail_view, name='company_detail'),
    path('<int:company_id>/add_branch/',
         create_branch, name='add_branch'),
    path('branch/<int:branch_id>/', branch_detail_view, name='branch_detail'),

]
