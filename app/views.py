from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
import django.contrib.auth as auth
import requests
import json
from collections import OrderedDict
from django.contrib import messages
from django.core import serializers
from rest_framework import viewsets
from openpyxl import load_workbook
from .models import NewUser, MyUser, Agency, Plan, Family, INF_details, NOR_details, JSON_To_NewUser, JSON_to_MyUser
from .serializers import MyUserSerializer, AgencySerializer, PlanSerializer, FamilySerializer, InfdetailSerializer, NordetailSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
import app.models
import app.models as table
import random
import json
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
        serializer.save()


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




def agency_generator(request):
    agencies = ['KT', 'SKT', 'LG', 'CKT', 'CSKT', 'CLG']
    agency1 = Agency(Agency_name=agencies[0], Agency_phone=140)
    agency1.save()
    agency2 = Agency(Agency_name=agencies[1], Agency_phone=160)
    agency2.save()
    agency3 = Agency(Agency_name=agencies[2], Agency_phone=180)
    agency3.save()
    agency4 = Agency(Agency_name=agencies[3], Agency_phone=200)
    agency4.save()
    agency5 = Agency(Agency_name=agencies[4], Agency_phone=220)
    agency5.save()
    agency6 = Agency(Agency_name=agencies[5], Agency_phone=240)
    agency6.save()
    return render(request,'app/make_data.html')

def plan_generator(request):
    return render(request,'app/make_data.html')

def make_user():
    rand_phonenum = 29823081
    family_id = 0
    agencies = ['KT', 'SKT', 'LGU+', 'C_SKT', 'C_KT', 'C_LGU+']
    user_contents = ['통화', '영상시청', '커뮤니티', '게임', '웹서핑', '작업']
    plan_key = []
    data_useage_6 = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}

    for i in range(1001, 1019 + 1): plan_key.append(i)
    for i in range(2001, 2048 + 1): plan_key.append(i)
    for i in range(3001, 3052 + 1): plan_key.append(i)
    for i in range(4001, 4006 + 1): plan_key.append(i)
    for i in range(5001, 5019 + 1): plan_key.append(i)
    for i in range(6001, 6025 + 1): plan_key.append(i)
    for i in range(1101, 1115 + 1): plan_key.append(i)
    for i in range(2101, 2113 + 1): plan_key.append(i)
    for i in range(3101, 3120 + 1): plan_key.append(i)
    plan_key.append(4101)
    for i in range(5101, 5102 + 1): plan_key.append(i)
    for i in range(6101, 6102 + 1): plan_key.append(i)

    infp = INF_details(Plan_ID=3, Plan_name='test', Plan_cost=300,
                       Agency_name=Agency.objects.get(Agency_name=agencies[0]),
                       Call_Limit=3, Message_Limit=3,
                       Month_limit=300, Day_limit=2)
    infp.save()
    for i in range(0, 10000):
        rand_phonenum += random.randint(1, 2)
        name_selector1 = random.randint(0, 29)
        name_selector2 = random.randint(0, 45)
        name_selector3 = random.randint(0, 45)
        content_selector = random.randint(0, 5)
        plan_selector = random.randint(0, 221)
        message_dif = random.randint(0, 15)
        call_dif = random.randint(0, 10)

        if (plan_key[plan_selector] % 1000) // 100 == 0:
            plan = NOR_details.objects.get(Plan_ID=plan_key[plan_selector])
            for i in range(1, 6 + 1):
                data_dif = random.randint(0, 5) / 10
                data_useage_6[str(i)] = abs(plan.Total_limit - data_dif)
            myuser = table.MyUser(phonenum=str(rand_phonenum),
                                  name=last_name[name_selector1] + first_name[name_selector2] + first_name[
                                      name_selector3],
                                  Plan_name=plan,
                                  data_useage=json.dumps(data_useage_6),
                                  message_useage=abs(plan.Message_Limit - message_dif),
                                  call_useage=abs(plan.Call_Limit - call_dif),
                                  User_contents=user_contents[content_selector],
                                  )
        else:
            plan = INF_details.objects.get(Plan_ID=plan_key[plan_selector])
            for i in range(1, 6 + 1):
                data_dif = random.randint(-3, 5)
                data_useage_6[str(i)] = plan.Month_limit + data_dif
            myuser = table.MyUser(phonenum=str(rand_phonenum),
                                  name=last_name[name_selector1] + first_name[name_selector2] + first_name[
                                      name_selector3],
                                  Plan_name=plan,
                                  data_useage=json.dumps(data_useage_6),
                                  message_useage=abs(plan.Message_Limit - message_dif),
                                  call_useage=abs(plan.Call_Limit - call_dif),
                                  User_contents=user_contents[content_selector],
                                  )

        myuser.save()
        if (i % 2) == 0:
            family_id += 1
            Agency_selector = random.randint(0, 8) % 6
            family = table.Family(Family_User=myuser,
                                  Family_id=family_id,
                                  agency_name=Agency.objects.get(Agency_name=agencies[Agency_selector])
                                  )
            family.save()


# 유저, 통신사, 가족 데이터 생성
def testleft(request):
    make_plan_table()
    return render(request,'app/make_data.html')

def recommend():    # 요금제 추천해주는 시스템.
    return 0

def testright(request):
    make_user()
    return render(request,'app/make_data.html')




def make_plan_json(Plan_list):
    plan_data = OrderedDict()
    plan_data["Plan_ID"] = Plan_list[0]
    plan_data["Plan_name"] = Plan_list[2]
    plan_data["Plan_cost"] = Plan_list[3]
    plan_data["Agency_name"] = Plan_list[1]
    plan_data["Call_Limit"] = Plan_list[8]
    plan_data["Message_Limit"] = Plan_list[9]

    if plan_data["Call_Limit"] == '기본제공':
        plan_data["Call_Limit"] = 999999

    elif plan_data["Call_Limit"] == "X":
        plan_data["Call_Limit"] = 0

    if plan_data["Message_Limit"] == '기본제공':
        plan_data["Message_Limit"] = 999999

    elif plan_data["Message_Limit"] == "X":
        plan_data["Message_Limit"] = 0

    return plan_data

def make_inf_json(Plan_list, planjson):
    planjson["Month_limit"] = Plan_list[6]
    planjson["Day_limit"] = Plan_list[7]

    if planjson["Month_limit"] == '기본제공':
        planjson["Month_limit"] = 999999.

    elif planjson["Month_limit"] == "X":
        planjson["Month_limit"] = 0.

    if planjson["Day_limit"] == "X":
        planjson["Day_limit"] = 0.
    infjson = json.dumps(planjson, ensure_ascii=False, indent="\t").encode('utf-8')


    return infjson

def make_nor_json(Plan_list, planjson):
    planjson["Total_limit"] = Plan_list[6]

    if planjson["Total_limit"] == '기본제공':
        planjson["Total_limit"] = 999999.

    elif planjson["Total_limit"] == "X":
        planjson["Total_limit"] = 0.
    norjson = json.dumps(planjson, ensure_ascii=False, indent="\t").encode('utf-8')

    return norjson


def make_plan_table():
    load_wb = load_workbook("app/static/app/data.xlsx", data_only=True)
    load_ws = load_wb['Sheet1']
    all_values = []
    for row in load_ws.rows:
        row_value = []
        for cell in row:
            row_value.append(cell.value)
        all_values.append(row_value)
    all_values = all_values[2:]
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    for value in all_values:
        is_inf = value[4]
        plan_json = make_plan_json(value)
        inf_json = plan_json.copy()
        nor_json = plan_json.copy()

        inf_json = make_inf_json(value, inf_json)
        nor_json = make_nor_json(value,nor_json)

        if(is_inf == "O"):      #무한
            requests.post("http://127.0.0.1:8000/infapi/", headers=headers ,data=inf_json)
        else:                   #무제한 아닌거
            requests.post("http://127.0.0.1:8000/norapi/", headers=headers ,data=nor_json)




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
