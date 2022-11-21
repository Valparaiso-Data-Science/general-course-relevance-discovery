import re
from django.shortcuts import render, get_object_or_404
from .models import School, Catalog, Request
from django.views import generic
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


# Create your views here.

class SchoolCreate(CreateView):
    model = School
    fields = ['name', 'state']

    def get_success_url(self):
        return reverse_lazy('index')

class CatalogCreate(CreateView):
    model = Catalog
    fields = ['name', 'school', 'year', 'pdf', 'xml_file']

    def get_success_url(self):
        return reverse_lazy('index')

class RequestCreate(CreateView):
    model = Request
    fields = ['school', 'catalog', 'rq_type', 'search_terms', 'category']

    def get_success_url(self):
        return reverse_lazy('index')


def index(request):
    """View function for home page of site."""

    return render(request, 'index.html')


class SchoolListView(generic.ListView):
    model = School
    context_object_name = 'school_list'   # your own name for the list as a template variable
    #queryset = School.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #template_name = 'schools/my_arbitrary_template_name_list.html'  # Specify your own template name/location


class CatalogListView(generic.ListView):
    model = Catalog
    context_object_name = 'catalog_list'   # your own name for the list as a template variable
    #queryset = School.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #template_name = 'schools/my_arbitrary_template_name_list.html'  # Specify your own template name/location

