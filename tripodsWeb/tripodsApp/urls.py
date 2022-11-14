from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('schools/', views.SchoolListView.as_view(), name='schools'),
    path('catalogs/', views.CatalogListView.as_view(), name='catalogs'),
    path('schools/create/', views.SchoolCreate.as_view(), name='school-create'),
    path('catalogs/create/', views.CatalogCreate.as_view(), name='catalog-create'),
    path('requests/create/', views.RequestCreate.as_view(), name='request-create')
]
