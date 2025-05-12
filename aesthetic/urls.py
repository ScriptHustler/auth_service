from django.urls import path
from . import views

app_name='aesthetics'

urlpatterns = [
    path('', views.aesthetics_list,name="list"),
    path('<slug:slug>', views.aesthetic_page,name="page")
]