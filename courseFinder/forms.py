from django import forms
from django.forms import ModelForm
from .models import Request, Catalog

class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ('school', 'catalog', 'rq_type', 'search_terms', 'name', 'email')
        widgets = {
                'school': forms.Select(attrs={'class': 'form-control', 'placeholder': 'School'}),
                'catalog': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Catalog'}),
                'rq_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Request Type'}),
                'search_terms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter your search terms seperated by commas, i.e. "data, data science, data visualization"'}),
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please provide a short description of the subject of your search terms, i.e. "data science, theatre, cinema, korean"'}),
                #'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please input an email to send your results to."'}),
            }

class CatalogForm(ModelForm):
    school = forms.TextInput()
    year = forms.NumberInput()
    xml_file = forms.FileField()

    class Meta:
        model = Catalog
        fields = ('school', 'year', 'xml_file')
        
        widgets = {
                'school': forms.Select(attrs={'class': 'form-control', 'placeholder': 'School'}),
                'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
                #'xml_file': forms.FileField(label='Select a file', help_text='Upload a XML of your course catalog'),
            }
