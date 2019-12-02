from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
import django.contrib.auth as auth

from .models import MyUser, LoginForm

def index(request):
    return render(request,'app/index.html')

def newuserform(request):
    return render(request, 'app/newuser_form.html')

def dashboard(request):
    user_id = request.session['user_id']
    user = authenticate(request, username=user_id)
    context = {'user': user}
    # context = {'user_name' : user.name, 'phonenum' : user.phonenum, 'data_useage' : user.data_useage}
    print(context)
    return render(request, 'app/dashboard.html', context)

def recommend():    # 요금제 추천해주는 시스템.

    return 0


def signin(request):
    if request.COOKIES.get('username') is not None:
        username = request.COOKIES.get('username')
        user = authenticate(request, username=username)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.phonenum
            return redirect(request, 'dashboard')

    elif request.method =="POST":
        form = LoginForm(request.POST)
        phonenum = request.POST['phonenum']       #PK
        user = authenticate(request ,username=phonenum)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.phonenum

            if request.POST.get("keep_login") == "TRUE":
                response = redirect(request , 'dashboard')
                response.set_cookie(phonenum)
                return response
            return redirect('dashboard')
        else:
            return HttpResponse('로그인 실패, 다시 시도 해보세요')
    else:
        form = LoginForm()
        return render(request, 'app/login.html',{'form' : form})

#logout delete cookie
def logout(request):
    del request.session['user_id']
    response = render(request,'app/index.html')
    response.delete_cookie('username')
    auth.logout(request)
    return response
# Create your views here.
