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
import app.models
import app.models as table
import random
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DB_project.settings')


last_name = ['김' , '이' , '박' , '최' , '정'
    , '강' , '조' , '윤' , '장' , '임' , '오'
    , '한' , '신' , '서' , '권' , '황' , '안'
    , '송' , '유' , '홍' , '전' , '고' , '문'
    , '손' , '양' , '배' , '조' , '백' , '허'
    , '남'] # 30종
first_name = ['민' , '현' , '동' , '인'
    , '현' , '재' , '우' , '건' , '준'
    , '영' , '성' , '진' , '정' , '수'
    , '광' , '호' , '중' , '훈' , '후'
    , '상' , '연' , '철' , '아' , '윤'
    , '유' , '자' , '도' , '은' , '승'
    , '남' , '식' , '일' , '병' , '혜'
    , '미' , '환' , '숙' , '지'
    , '희' , '순' , '서' , '빈'
    , '하' , '공' , '안' , '원'] # 46종

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
        request.session['newuser'] = newuser.toJSON() #json 변환.
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

# 유저, 통신사, 가족 데이터 생성
def data_generate(request):
    rand_phonenum = 29823081
    Family_id = 0
    Agencies = ['KT', 'SKT', 'LG', 'CKT', 'CSKT', 'CLG']
    User_contents = ['통화', '영상시청', '커뮤니티', '게임', '웹서핑', '작업']

    Agency1 = Agency(Agency_name=Agencies[0], Agency_phone=140)
    Agency1.save()
    Agency2 = Agency(Agency_name=Agencies[1], Agency_phone=160)
    Agency2.save()
    Agency3 = Agency(Agency_name=Agencies[2], Agency_phone=180)
    Agency3.save()
    Agency4 = Agency(Agency_name=Agencies[3], Agency_phone=200)
    Agency4.save()
    Agency5 = Agency(Agency_name=Agencies[4], Agency_phone=220)
    Agency5.save()
    Agency6 = Agency(Agency_name=Agencies[5], Agency_phone=240)
    Agency6.save()
    infp = INF_details(Plan_name='test', Agency_name=Agency6,
                       Call_Limit=3, Message_Limit=3,
                       Month_limit=300, Day_limit=2)
    infp.save()
    for i in range(0, 10000):
        rand_phonenum += random.randint(1, 2)
        name_selector1 = random.randint(0, 29)
        name_selector2 = random.randint(0, 45)
        name_selector3 = random.randint(0, 45)
        content_selector = random.randint(0,5)
        myuser = table.MyUser(phonenum=str(rand_phonenum),
                              name=last_name[name_selector1]+first_name[name_selector2]+first_name[name_selector3],
                              Plan_name=infp,
                              data_useage='랜덤 생성 예정',
                              message_useage='랜덤 생성 예정',
                              call_useage='랜덤 생성 예정',
                              User_contents=User_contents[content_selector],
                              )
        myuser.save()
        if (i%2) == 0:
            Family_id += 1
            Agency_selector = random.randint(0, 8) % 6
            family = table.Family(Family_User=myuser,
                                  Family_id=Family_id,
                                  agency_name=Agency.objects.get(Agency_name=Agencies[Agency_selector])
                                  )
            family.save()

    return render(request,'app/index.html')

def plan_data():
    random.randint()


def recommend():    # 요금제 추천해주는 시스템.
    return 0


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
