from django.shortcuts import render , redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login , logout
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your views here.

def index(request):
    name = "Admin"
    email = "admin@gmail.com"
    activitys = [
        'football',
        'running',
        'tennis'
    ]
    return render(request , 'index.html' ,{
        'name': name,
        'email': email,
        'activitys': activitys,
    })

def hello(request,id):
    url_id = 'Url you id : ' + str(id)
    return HttpResponse(url_id);

def article(request , year , slug):
    return HttpResponse("Article" + str(year) + str(slug));

def login_view(request):
    if request.method == "POST":
        # เอาข้อมูลที่ส่งมาหลังจาก user กด submit
        form = AuthenticationForm(data=request.POST)
        # ตรวจสอบว่ามีข้อมูลไหม
        if form.is_valid():
            # get ข้อมูลที่กรอกมาจาก form
            user = form.get_user()
            # เช็คว่ามีใน db ไหม
            login(request, user)
            # return HttpResponseRedirect(reverse('book:index'))
            # หรือใช้ 
            return redirect('book:index')
    else:
        # สร้าง form login
        form =AuthenticationForm()
    return render(request , 'account/login.html' , {
            'form': form,
    })

def logout_view(request):
        if request.method == 'POST':
            logout(request)
            return redirect('myapp:index')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('book:index')
    else:
        form = UserCreationForm()
    return render(request , 'account/signup.html', {
        'form': form,
    })
