from django.shortcuts import render
from .models import School
from django.views.generic.edit import CreateView
from .forms import RequestForm, CatalogForm
import shutil
from django.db import connection
from django.urls import reverse_lazy
from subprocess import call
import pandas as pd
import importlib

#from tripodscode.analysis import sendResponse
# from email.mime.multiparti mport MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib


class SchoolCreate(CreateView):
    model = School
    fields = ['name', 'state']

    def get_success_url(self):
        return reverse_lazy('index')

def catalogForm(request):
    #submitbutton= request.POST.get("submit")
    form = CatalogForm(request.POST, request.FILES)
    print(request.FILES)
    if request.method == 'POST':
        
        if form.is_valid():
            form.save()   

    context = {
        'form':form
    }
    return render(request, 'catalogForm.html', context)

def results(request):
    csv_file = "/Users/cnguyen/testing/tripodsWeb/tripodscode/analysis copy/final_resultstest_save_course_recs.csv"
    data = pd.read_csv(csv_file)
    data_string = data[['CourseID','Descriptions','FoundTerms']]
    datahtml = data_string.to_html()
    text_file = open("courseFinder/templates/results.html", "w")
    text_file.write(datahtml)
    text_file.close()
    return render(request,'results.html')

def index(request):
    submitbutton= request.POST.get("submit")
    name=''
    school=''
    catalog=''
    search_terms=''
    rq_type=''
    email=''
    form = RequestForm(request.POST or None)

    if request.method == 'POST':
        submitbutton = True
        school = request.POST.get('school')
        catalog = request.POST.get('catalog')
        rq_type = request.POST.get('rq_type')
        search_terms = request.POST.get('search_terms')
        name = request.POST.get('name')
        email = request.POST.get('email')

        form = RequestForm(request.POST)

        if form.is_valid():

            with connection.cursor() as c:
                c.execute('SELECT xml_file FROM courseFinder_catalog WHERE id = %s', [catalog])
                xml_path = c.fetchone()
            cleanXMLPath(xml_path)

            with open('search_terms.txt', 'w') as f:
                f.write(search_terms)
            #os.system('python3 main.py')
            call(["python3", "main.py"], cwd='/Users/cnguyen/testing/tripodsWeb/tripodscode/source/')
            call(["python3", "main.py"], cwd='/Users/cnguyen/testing/tripodsWeb/tripodscode/analysis copy/')
            

            # csv_file = "/Users/cnguyen/testing/tripodsWeb/tripodscode/analysis copy/final_resultstest_save_course_recs.csv"
            # data = pd.read_csv(csv_file)
            # data_string = data[['CourseID','Descriptions','FoundTerms']]
            # datahtml = data_string.to_html()
            # text_file = open("results.html", "w")
            # text_file.write(datahtml)
            # text_file.close()
            
            form.save()


    context = {
        'form': form,
        'name': name,
        'school': school,
        'catalog': catalog,
        'rq_type': rq_type,
        'search_terms': search_terms,
        'submitbutton': submitbutton,
        'email': email,
        #'loaded_data':datahtml
    }
    return render(request, 'index.html', context)

def cleanXMLPath(xml_path):
    print(xml_path)
    d = str(xml_path)
    s = ['(', ')', ',', '\'']
    final = d.translate({ord(x): '' for x in s})
    print(final)
    src = '/Users/cnguyen/testing/tripodsWeb/'+final
    print(src)
    dst = '/Users/cnguyen/testing/tripodsWeb/tripodscode/XMLs/requested.xml'
    shutil.copy(src, dst)
    return final




