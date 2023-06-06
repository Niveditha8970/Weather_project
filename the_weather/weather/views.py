import requests
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CityForm,UserRegister
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def get_html_content(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def dash(request):
    result = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        # extract region
        result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        # extract temperature now
        result['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        # get the day, hour and actual weather
        result['dayhour'], result['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split(
            '\n')
    return render(request, 'dash.html', {'result': result})


def user_register(request):

    if request.method=="POST":
        regfmdata=UserRegister(request.POST)
        message={}
        if regfmdata.is_valid():
            regfmdata.save()
            message['msg']="Congratulation, Register Done Successfully. Please Login"
            message['x']=1
            return render(request, 'register_success.html', message)
    
        else:
            message['msg']="Failed to Register User. Please try Again"
            message['x']=0
            return render(request, 'register_success.html', message)
    
    else:
        
        regfm=UserRegister()
        content={}
        content['regfmdata']=regfm
        return render(request,'register.html',content)
    
def user_login(request):
    fmlog=AuthenticationForm()
    content={}
    content['logfmdata']=fmlog
    if request.method=="POST":
        logfmdata=AuthenticationForm(request=request,data=request.POST)
        if logfmdata.is_valid():
            uname=logfmdata.cleaned_data['username']
            upass=logfmdata.cleaned_data['password']
            r=authenticate(username=uname,password=upass)
            if r is not None:
                login(request,r)#start session and store id of logged in user
                return redirect('/dash')
        else:
            content['msg']="Invaild username and Password!!!"
            return render(request,'index.html',content)
    else:
        return render(request,'index.html',content)
    
def user_logout(request): #it destroy session or data stored in session

    logout(request)
    return redirect('/')

