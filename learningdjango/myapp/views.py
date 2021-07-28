from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request ,id):
    id = str(id)
    name = "Admin"
    email = "admin@gmail.com"
    activitys = [
        'football',
        'running',
        'tennis'
    ]
    return render(request , 'index.html' ,{
        'id': id,
        'name': name,
        'email': email,
        'activitys': activitys,
    })

def hello(request,id):
    url_id = 'Url you id : ' + str(id)
    return HttpResponse(url_id);

def article(request , year , slug):
    return HttpResponse("Article" + str(year) + str(slug));
