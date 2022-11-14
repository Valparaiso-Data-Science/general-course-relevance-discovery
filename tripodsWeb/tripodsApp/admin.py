from django.contrib import admin
from .models import School, Request, Catalog
# Register your models here.

#admin.site.register(School)
#admin.site.register(Request)
#admin.site.register(Catalog)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')

admin.site.register(School, SchoolAdmin)

class RequestAdmin(admin.ModelAdmin):
    list_display = ('school', 'catalog', 'rq_type')

admin.site.register(Request, RequestAdmin)

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('school', 'year')

admin.site.register(Catalog, CatalogAdmin)