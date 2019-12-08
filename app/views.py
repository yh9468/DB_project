from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
import django.contrib.auth as auth
import requests
from django.contrib import messages
from django.core import serializers
from rest_framework import viewsets
from .models import NewUser, MyUser, Agency, Plan, Family, INF_details, NOR_details, JSON_To_NewUser, JSON_to_MyUser
from .serializers import MyUserSerializer, AgencySerializer, PlanSerializer, FamilySerializer, InfdetailSerializer, NordetailSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


#restful API view 들
class MyUserView(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class =MyUserSerializer

    def perform_create(self, serializer):
        serializer.save(plan=self.request.agency, family=self.request.family)


class AgencyView(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    def perfom_create(self, serializer):
        serializer.save()

class PlanView(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class FamilyView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class InfdetailView(viewsets.ModelViewSet):
    queryset = INF_details.objects.all()
    serializer_class = InfdetailSerializer

class NordetailView(viewsets.ModelViewSet):
    queryset = NOR_details.objects.all()
    serializer_class = NordetailSerializer

def make_data(request):
    return render(request,'app/make_data.html')

def index(request):
    return render(request,'app/index.html')

def newuserform(request):
    if request.method == 'POST':
        name =request.POST['name']
        age = request.POST['age']
        main_content = request.POST['main_content']
        data_usage = request.POST['data_usage']
        Agency_name = request.POST['Agency_name']
        Check_INF = request.POST['Check_INF']
        request.session['user_id'] = "0000"
        newuser = NewUser('0000',name, age, main_content, data_usage, Agency_name, Check_INF)
        request.session['newuser'] = newuser.toJSON()           #json 변환.
        return redirect('dashboard')
    # get
    else:
        return render(request,'app/newuser_form.html')

def dashboard(request):
    user_id = request.session['user_id']
    # 새로운 유저인 경우.
    if user_id == "0000":
        newuser = request.session['newuser']
        newuser = JSON_To_NewUser(newuser)
        context = {'user' : newuser}
        return render(request, 'app/dashboard.html', context)

    # 로그인 하는 경우
    else:
        response = requests.get(f'http://127.0.0.1:8000/api/{user_id}/')
        user = response.json()
        user = JSON_to_MyUser(user)
        print(f"User : {user}")
        context = {'user': user}
        return render(request, 'app/dashboard.html', context)


def recommend():    # 요금제 추천해주는 시스템.
    return 0

def testleft(request):
    print("왼쪽 버튼을 눌렀습니다")
    return render(request,'app/make_data.html')

def testright(request):
    print("오른쪽 버튼을 눌렀습니다")
    return render(request,'app/make_data.html')

def signin(request):
    if request.COOKIES.get('username') is not None:
        username = request.COOKIES.get('phonenum')
        password = request.COOKIES.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.phonenum
            return redirect(request, 'dashboard')
        else:
            return render(request,'app/login.html')

    elif request.method =="POST":
        phonenum = request.POST['phonenum']       #PK
        password = request.POST['password']
        user = authenticate(request ,username=phonenum, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.phonenum
            request.session['password'] = user.password

            if request.POST.get("keep_login") == "TRUE":
                response = redirect(request , 'dashboard')
                response.set_cookie('phonenum', phonenum)
                response.set_cookie('password', password)
                return response
            return redirect('dashboard')
        else:           #로그인 실패
            return render(request, 'app/login.html'), {'error':'username or password is incorrect'}

    else:           #get
        return render(request, 'app/login.html')

#logout delete cookie
def logout(request):
    del request.session['user_id']
    return redirect('signin')
# Create your views here.
