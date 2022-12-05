from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogForm/',views.catalogForm, name='catalogForm'),
    path('schools/create/', views.SchoolCreate.as_view(), name='school_form'),
    path('results', views.results, name='results'),
]
