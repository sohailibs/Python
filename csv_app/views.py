from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from .forms import InputForm
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
import os

# Create your views here.
def home_view(request):
    context = {}
    context['form'] = InputForm()
    if request.method == "POST":
        # Get the posted form
        Form = InputForm(request.POST)

        if Form.is_valid():
            search_term = Form.cleaned_data['search_term']

            """Generate a url from search term"""
            template = "https://www.google.co.in/search?biw=1366&bih=657&ei=8wEHYJGGHb2f4-EPuo-N8AU&q={}"
            search_term = search_term.replace(' ', '+')
            # add term query to url
            url = template.format(search_term)
            result = requests.get(url)
            soup = BeautifulSoup(result.text, 'html.parser')
            # links = soup.select('.yuRUbf, a')
            links = soup.select('.tF2Cxc, a')
            records = []
            substr = "https"
            for link in links:
                link = link.get('href').replace('/url?q=', '')
                if link.__contains__(substr):
                    print(link)
                    result = (link,)
                    records.append(result)
                    with open('media/links8.csv', 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Url'])
                        writer.writerows(records)

    else:
        # MyLoginForm = Loginform()
        redirect('/forms')
    # Table(result)
    return render(request, "forms.html", context)


def save_file(request):
   # data = open(os.path.join(settings.PROJECT_PATH,'data/table.csv'),'r').read()
    file_path =settings.MEDIA_ROOT +'/'+ 'links8.csv'
    response = HttpResponse(file_path, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=links8.csv'
    return response


# Simple CSV Read Operation
def Table(request):
    file_path = settings.MEDIA_ROOT + '/' + 'links8.csv'
    df = pd.read_csv(file_path)
    # df = pd.read_csv("django_csv/media/links8.csv")
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
    return render(request, 'table.html', context)



