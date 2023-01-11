from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Profile
import random, json
import requests
import http.client
from django.conf import settings
import datetime
from django.contrib.auth import authenticate, login
# Create your views here.
def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey=settings.API_KEY
    headers = { 'content-Type': "application/json" }
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    url=url.replace(" ", '')
    conn.request('GET', url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None


def home(request):
            
    return render(request, 'home.html')

def login_attempt(request):
    if request.method=='POST':
        mobile=request.POST.get('mobile')

        user=Profile.objects.filter(mobile=mobile).first()
        
        if user is None:
            context={'message':'User does not exists', 'class':'danger'}
            return render(request, 'register.html', context)
        
        otp=str(random.randint(1000,9999))
        user.otp=otp
        user.save()
        send_otp(mobile, otp)
        print(otp)
        print(otp)
        request.session['mobile']=mobile
        return redirect('login_otp')

    return render(request, 'login.html')

def login_otp(request):
    mobile=request.session['mobile']
    context={'mobile':mobile}
    if request.method=='POST':
        otp=request.POST.get('otp')
        profile=Profile.objects.filter(mobile=mobile).first()

        if otp==profile.otp:
            user=User.objects.get(id=profile.user.id)
            
            login(request, user)
            return redirect('home')

        else:
            context={'message':'OTP entered is wrong', 'class':'danger'}
            return render(request, 'login_otp.html', context)
    return render(request, 'login_otp.html', context)
    
def register(request):
    if request.method=='POST':
        email=request.POST.get('email')
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')

        check_user=User.objects.filter(email=email).first()
        check_profile=Profile.objects.filter(mobile=mobile).first()

        if check_user or check_profile :
            context={'message':'User already exists', 'class':'danger'}
            return render(request, 'register.html', context)
        user=User(email=email, first_name=name)
        user.save()

        otp=str(random.randint(1000, 9999))

        profile=Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile']=mobile

        return redirect('otp')
    return render(request, 'register.html')

def otp(request):
    mobile=request.session['mobile']
    context={'mobile':mobile}
    if request.method=='POST':
        otp=request.POST.get('otp')
        profile=Profile.objects.filter(mobile=mobile).first()

        if otp==profile.otp:
            return redirect('home')
        else:
            context={'message':'Entered OTP is Wrong', 'class':'danger', 'mobile':mobile}
            return render(request, 'otp.html', context)
    return render(request, 'otp.html', context)

def weather(request):
    if request.method=='POST':
        city=request.POST.get('city') 
    
    else:
        city='london'

    apikey='*************'
    URL="https://api.openweathermap.org/data/2.5/weather"
    PARAMS={"q":city, 'apikey':apikey, 'units':'metric'}
    r=requests.get(url=URL, params=PARAMS)  
    res=r.json()
    print(res)
    description=res['weather'][0]['description']
    icon=res['weather'][0]['icon']
    temp=res['main']['temp']
    day=datetime.date.today()

    # conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")
    # url = "https://community-open-weather-map.p.rapidapi.com/weather"
    # querystring = {"q":"London,uk"}
    # headers = {
    # 'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    # 'x-rapidapi-key': "*****"
    # }
    # conn.request("GET",url,params=querystring, headers=headers)
    # res = conn.getresponse()
    # data=res.read()
    # print(data)
    # description=data['weather'][0]['description']
    # icon=data['weather'][0]['icon']
    # temp=data['main']['temp']

    # import http.client

    # conn = http.client.HTTPSConnection("community-open-weather-map.p.rapidapi.com")

    # headers = {
    # 'X-RapidAPI-Key': "*********",
    # 'X-RapidAPI-Host': "community-open-weather-map.p.rapidapi.com"
    # }

    # conn.request("GET", "/weather?q=London%2Cuk&lat=0&lon=0&callback=test&id=2172797&lang=null&units=imperial&mode=xml", headers=headers)

    # res = conn.getresponse()
    # data = res.read()
    # print(data.decode('utf-8'))
    
    
    

    # description=r['weather'][0]['description']
    # icon=r['weather'][0]['weather']
    # temp=r['main']['temp']
    return render(request, 'weather.html', {'description':description, 'icon':icon, 'temp':temp, 'day':day, 'city':city})


