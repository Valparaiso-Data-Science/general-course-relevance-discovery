from distutils.command.upload import upload
from unittest.util import _MAX_LENGTH
from django.db import models
from django.urls import reverse
'''
Table 1: Schools & Catalogs
'''

class School(models.Model):
    us_states = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
    name = models.CharField('Name', max_length=200, default=None)
    state = models.CharField('State', max_length=2, choices = us_states, default=None)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)])

    class meta:
        ordering = ['name']


class Catalog(models.Model):
    #name = models.CharField('Name', max_length=200, default='catalog')
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=None)
    year = models.IntegerField('Year', default=None)
    xml_file = models.FileField(upload_to="courseFinder/media/",default=None)
 

    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1}'.format(self.school, self.year)
    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)]) 
    
    class meta:
        ordering = ['school']

'''
Table 2: Requests
'''
class Request(models.Model):
    REQUEST_TYPES = (
        ('Pu', 'Public'),
        ('R', 'Research'),
        ('Pr', 'Private'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=None)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, default=None)
    rq_type =  models.CharField('Request Type', max_length=2, choices=REQUEST_TYPES)
    search_terms = models.TextField('Search Terms')
    name =  models.CharField('Category', max_length=200)
    email = models.EmailField(max_length=254)

    def __str__(self):
        """String for representing the Model object."""
        return '{0} {1} {2} {3}'.format(self.school, self.catalog, self.rq_type, self.name)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('model-detail-view', args=[str(self.id)]) 