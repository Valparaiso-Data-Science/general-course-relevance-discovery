from dataclasses import field
from typing_extensions import Required
from django import forms
from .models import School, Catalog, Request

class FullRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            'school',
            'catalog',
            'rq_type',
            'category',
            'search_terms',

        )




class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = (
            'name',
            'state',
        )


class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = (
            'name',
            'school',
            'year',
            'pdf'
        )


