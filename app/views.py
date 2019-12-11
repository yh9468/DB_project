from django.shortcuts import render, redirect
import urllib
from django.http import HttpResponse, HttpResponseRedirect
import string
from django.contrib.auth import login, authenticate
import django.contrib.auth as auth
import requests
from rest_framework import generics
import json
from collections import OrderedDict, Counter
from django.contrib import messages
from django.core import serializers
from rest_framework import viewsets
from openpyxl import load_workbook
from .models import NewUser, MyUser, Agency, Plan, Family, INF_details, NOR_details, JSON_To_NewUser, JSON_to_MyUser, Use_detail, JSON_to_use
from .serializers import MyUserSerializer, AgencySerializer, PlanSerializer, FamilySerializer, InfdetailSerializer, NordetailSerializer, UseSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
import app.models
import app.models as table
from rest_framework.response import Response
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

class UsedetailView(viewsets.ModelViewSet):
    queryset = Use_detail.objects.all()
    serializer_class = UseSerializer
    def perform_create(self, serializer):
        serializer.save()

class Use_detail_List(generics.ListAPIView):
    serializer_class = UseSerializer
    def get_queryset(self):
        phonenum = self.kwargs['phonenum']
        return Use_detail.objects.filter(phonenum__phonenum=phonenum)


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
        Check_cheap = request.POST['Check_cheap']
        message_usage = request.POST['Message_usage']
        call_usage = request.POST['Call_usage']
        request.session['user_id'] = "0000"
        newuser = NewUser('0000',name, age, main_content, data_usage, call_usage, message_usage,
                          Agency_name, Check_INF, Check_cheap)
        request.session['newuser'] = newuser.toJSON()      #json 변환.

        if(Check_cheap == 'on'):
            request.session['is_cheap'] = True
        else:
            request.session['is_cheap'] = False
        if(Check_INF == 'on'):
            request.session['is_inf'] = True
        else:
            request.session['is_inf'] = False
        return redirect('dashboard')
    # get
    else:
        return render(request,'app/newuser_form.html')

def dashboard(request):
    user_id = request.session['user_id']
    is_cheap = request.session['is_cheap']
    # 새로운 유저인 경우.
    if user_id == "0000":
        is_inf = request.session['is_inf']
        newuser = request.session['newuser']
        newuser = JSON_To_NewUser(newuser)
        result2 = new_pop_best_plan(newuser.name, newuser.age, newuser.main_content, newuser.data_usage,
                          newuser.Call_usage, newuser.Message_usage, newuser.Agency_name, is_inf, is_cheap)
        result = newuser_mostplan(is_cheap, is_inf, int(newuser.data_usage) / 1024)

        context = {'user': newuser, 'mostplans': result, 'result2' : result2}
        return render(request, 'app/user_result.html', context)

    # 로그인 하는 경우
    else:
        is_change = request.session['is_change']

        recommend = pop_best_plan(user_id, is_change, is_cheap)
        recommend2 = most_plan(request)
        recommend3 = recommend2[1][0]
        recommend2 = recommend2[0][0]
        user_response = requests.get(f'http://127.0.0.1:8000/api/{user_id}/')
        user = user_response.json()
        user = JSON_to_MyUser(user)

        use_response = requests.get(f'http://127.0.0.1:8000/useapi/{user.phonenum}')
        use = use_response.json()
        use = JSON_to_use(use)

        if((user.Plan_ID_id % 1000) // 100 == 0):       #nor
            plan_response = requests.get(f'http://127.0.0.1:8000/norapi/{user.Plan_ID_id}')
            plan_response = plan_response.json()
            plan_data = plan_response['Total_limit'] * 12
        else:
            plan_response = requests.get(f'http://127.0.0.1:8000/infapi/{user.Plan_ID_id}')
            plan_response = plan_response.json()
            monthlimit = plan_response['Month_limit']
            if plan_response['Month_limit'] == 999999:
                monthlimit = 300
            plan_data = monthlimit * 12 + plan_response['Day_limit'] * 365

        context = {'user': user, 'use': use, 'plan_data': plan_data, 'recommend': recommend, 'recommend2' : recommend2, 'recommend3': recommend3}

        return render(request, 'app/dashboard.html', context)




def recommend():    # 요금제 추천해주는 시스템.
    return 0

def agency_generator():
    agencies = ['KT', 'SKT', 'LGU+', 'C_SKT', 'C_KT', 'C_LGU+']
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

def plan_generator(request):
    return render(request,'app/make_data.html')

# 유저, 통신사, 가족 데이터 생성
def make_plan_agency_btn(request):
    agency_generator()
    make_plan_table()
    return render(request,'app/make_data.html')

def make_user_btn(request):
    make_user()
    return render(request,'app/make_data.html')

def make_family_btn(request):
    make_family()
    return render(request, 'app/make_data.html')

def make_user():
    plan_key = []
    _LENGTH = 8
    string_pool = string.digits
    agencies = ['KT', 'SKT', 'LGU+', 'C_SKT', 'C_KT', 'C_LGU+']
    user_contents = ['통화', '영상시청', '커뮤니티', '게임', '웹서핑', '작업']
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    family_response = requests.get("http://127.0.0.1:8000/familyapi")
    family_json = family_response.json()
    family_length = len(family_json)

    user_response = requests.get("http://127.0.0.1:8000/api")
    user_json = user_response.json()
    user_length = len(user_json)
    print(user_length)

    norplan = requests.get("http://127.0.0.1:8000/norapi/")
    norplan = norplan.json()

    infplan = requests.get("http://127.0.0.1:8000/infapi/")
    infplan = infplan.json()

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

    for i in range(0, 5000):
        data_usage = OrderedDict()
        rand_phonenum = ""
        use_max = 0
        for k in range(_LENGTH):
            rand_phonenum+=random.choice(string_pool)
        name_selector1 = random.randint(0, 29)
        name_selector2 = random.randint(0, 45)
        name_selector3 = random.randint(0, 45)
        content_selector = random.randint(0, 5)
        plan_selector = random.randint(0, 221)
        message_usage = random.randint(1,300)
        call_usage = random.randint(10,250)
        user_data = OrderedDict()

        if (plan_key[plan_selector] % 1000) // 100 == 0:
            plan = norplan
        else:
            plan = infplan

        for plane_info in plan:
            if plane_info["Plan_ID"] == plan_key[plan_selector]:
                plan_data = plane_info

        if (plan_key[plan_selector] % 1000) // 100 == 0:
            for data_usage_1 in range(0, 12):
                data_dif = random.randint(0, 50) / 100
                data_usage[month[data_usage_1]] = round(abs(plan_data["Total_limit"] - data_dif),2)
                use_max = max(use_max, data_usage[month[data_usage_1]])
        else:
            for data_usage_1 in range(0, 12):
                data_dif = random.randint(-1, 20)
                if plan_data["Month_limit"] == 999999:
                    data_usage[month[data_usage_1]] = round(abs(300 + random.randint(-200, 0)),2)
                else:
                    data_usage[month[data_usage_1]] = round(abs(plan_data["Month_limit"] + data_dif),2)
                use_max = max(use_max, data_usage[month[data_usage_1]])

        data_usage['Use_max'] = use_max
        user_data["phonenum"] = "010" + rand_phonenum
        user_data["name"] = last_name[name_selector1] + first_name[name_selector2] + first_name[name_selector3]
        if plan_data["age"] == 18:
            user_data["age"] = random.randint(10, 18)
        elif plan_data["age"] == 24:
            user_data["age"] = random.randint(19, 24)
        elif plan_data["age"] == 65:
            user_data["age"] = random.randint(65, 100)
        else:
            user_data["age"] = random.randint(10, 100)

        user_data["Plan_ID"] = plan_key[plan_selector]
        user_data["message_usage"] = abs(message_usage)
        user_data["call_usage"] = abs(call_usage)
        user_data["User_contents"] = user_contents[content_selector]
        user_data["password"] = "0000"
        Family_ID = random.randint(1, family_length + 1)
        user_data["Family_ID"] = Family_ID
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        user_json = json.dumps(user_data, ensure_ascii=False, indent="\t").encode('utf-8')
        requests.post("http://127.0.0.1:8000/api/", headers=headers, data=user_json)

        data_usage["phonenum"] = "010" + rand_phonenum
        data_usage = json.dumps(data_usage, ensure_ascii=False, indent="\t").encode('utf-8')
        requests.post("http://127.0.0.1:8000/useapi/",headers=headers, data=data_usage)

#family 2500 개씩 만들기.
def make_family():
    family_response = requests.get("http://127.0.0.1:8000/familyapi/")
    length = len(family_response.json())
    agencies = ['KT', 'SKT', 'LGU+', 'C_SKT', 'C_KT', 'C_LGU+']
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    for family_id in range(length+1 , length+2501):
        family_data = OrderedDict()
        family_data['Family_id'] = family_id
        family_data['agency_name'] = agencies[random.randint(0,8) % 6]
        family_data = json.dumps(family_data, ensure_ascii=False, indent="\t").encode('utf-8')
        requests.post("http://127.0.0.1:8000/familyapi/", headers=headers, data=family_data)


def make_plan_json(Plan_list):
    plan_data = OrderedDict()
    plan_data["Plan_ID"] = Plan_list[0]
    plan_data["Plan_name"] = Plan_list[2]
    plan_data["Plan_cost"] = Plan_list[3]
    plan_data["Agency_name"] = Plan_list[1]
    plan_data["Call_Limit"] = Plan_list[8]
    plan_data["Message_Limit"] = Plan_list[9]
    plan_data['age'] = Plan_list[5]

    if plan_data["Call_Limit"] == '기본제공':
        plan_data["Call_Limit"] = 999999

    elif plan_data["Call_Limit"] == "X":
        plan_data["Call_Limit"] = 0

    if plan_data["Message_Limit"] == '기본제공':
        plan_data["Message_Limit"] = 999999

    elif plan_data["Message_Limit"] == "X":
        plan_data["Message_Limit"] = 0

    if plan_data['age'] == "X":
        plan_data['age'] = 0

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
        if request.POST['is_change'] == 'on':
            is_change = True
        else:
            is_change = False

        if request.POST['is_cheap'] == 'on':
            is_cheap = True
        else:
            is_cheap = False
        user = authenticate(request ,username=phonenum, password=password)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.phonenum
            request.session['password'] = user.password
            request.session['is_cheap'] = is_cheap
            request.session['is_change'] = is_change

            if request.POST.get("keep_login") == "TRUE":
                response = redirect(request , 'dashboard')
                response.set_cookie('phonenum', phonenum)
                response.set_cookie('password', password)
                return response
            return redirect('dashboard')
        else:           #로그인 실패
            return render(request, 'app/login.html', {'error':'username or password is incorrect'})

    else:           #get
        return render(request, 'app/login.html')

#logout delete cookie
def logout(request):
    del request.session['user_id']
    return redirect('signin')
# Create your views here.

def most_plan(request):
    # 현재 접속중인 세션 기준으로 phonenum을 받아온다
    phonenum = request.session['user_id']
    # json 형식의 user_plan을 가져옴
    user_plan = requests.get("http://127.0.0.1:8000/api/" + phonenum)
    user_plan = user_plan.json()

    use_data = requests.get("http://127.0.0.1:8000/useapi/" + phonenum)
    use_data = use_data.json()

    # 유저의 데이터 사용량 기반 타겟 범위 설정
    user_data_useage = use_data[0]['Use_max']
    target_max = (lambda t_max: t_max+0.3 if t_max+0.3 <= 99999 else 99999)(user_data_useage)
    target_min = (lambda t_min: t_min-0.3 if t_min-0.3 >= 0 else 0)(user_data_useage)
    # 범위에 맞는 플랜을 모두 찾아온다
    # 타겟 값을 통해 폰번호를 추출 -> 폰번호로 다시 오브젝트 필터를 씌워서 plan 추출 -> 플랜 번호로 ->
    users_search = list(Use_detail.objects.filter(Use_max__gte=target_min, Use_max__lte=target_max).values('phonenum'))
    plan_id = []
    for item in users_search:
        plan_id.append(str(MyUser.objects.get(phonenum=item['phonenum']).Plan_ID))
    cnt = Counter(plan_id).most_common(2)
    print(cnt)
    # 리턴 형식은 tuples in list
    # Ex: [('순선택 100분 250MB', 37), ('LTE WARP 골든 150', 34)]
    return cnt

def newuser_mostplan(is_cheap, is_inf, use_data):
    target_max = (lambda t_max: t_max+0.3 if t_max+0.3 <= 99999 else 99999)(use_data)
    target_min = (lambda t_min: t_min-0.3 if t_min-0.3 >= 0 else 0)(use_data)
    users_search = list(Use_detail.objects.filter(Use_max__gte=target_min, Use_max__lte=target_max).values('phonenum'))
    plan_id = []
    for item in users_search:
        plan_id.append(MyUser.objects.get(phonenum=item['phonenum']).Plan_ID.Plan_ID)

    cnt = list(Counter(plan_id))
    # 무한, 알뜰폰 여부 체크
    result_id = []
    if (is_cheap is True) and (is_inf is True):
        for item in cnt:
            if len(result_id) == 2:
                break
            if item//100 == 41 or item//100 == 51 or item//100 == 61:
                result_id.append(item)
    elif (is_cheap is True) and (is_inf is False):
        for item in cnt:
            if len(result_id) == 2:
                break
            if item//100 == 40 or item//100 == 50 or item//100 == 60:
                result_id.append(item)
    elif (is_cheap is False) and (is_inf is True):
        for item in cnt:
            if len(result_id) == 2:
                break
            if item//100 == 11 or item//100 == 21 or item//100 == 31:
                result_id.append(item)
    elif (is_cheap is False) and (is_inf is False):
        for item in cnt:
            if len(result_id) == 2:
                break
            if item//100 == 10 or item//100 == 20 or item//100 == 30:
                result_id.append(item)

    result_plan = []
    for plan_id in result_id:
        result_plan.append(Plan.objects.get(Plan_ID=plan_id).__str__())
    return result_plan


def new_pop_best_plan(name, age, content, data_useage, call_useage, message_useage, family_agency, check_inf, check_cheaf):
    norplan = requests.get("http://127.0.0.1:8000/norapi/")  # 기본 요금제
    norplan = norplan.json()
    infplan = requests.get("http://127.0.0.1:8000/infapi/")  # 무제한 요금제
    infplan = infplan.json()

    best_plan = []

    for plan_info in norplan:
        # 가족 결합
        if not (family_agency == plan_info["Agency_name"]):
            continue
        if plan_info["age"] == 65:
            if age < 65:
                continue
        elif plan_info["age"] == 18:
            if age > 18:
                continue
        elif plan_info["age"] == 24:
            if (age < 19) or (age > 24):
                continue

        if data_useage < plan_info["Total_limit"]:
            if call_useage < plan_info["Call_Limit"]:
                if message_useage < plan_info["Message_Limit"]:
                    best_plan.append(plan_info)

    if check_inf:
        for plan_info in infplan:
            # 가족 결합
            if not (family_agency == plan_info["Agency_name"]):
                continue
            if plan_info["age"] == 65:
                if age < 65:
                    continue
            elif plan_info["age"] == 18:
                if age > 18:
                    continue
            elif plan_info["age"] == 24:
                if (age < 19) or (age > 24):
                    continue

            if call_useage < plan_info["Call_Limit"]:
                if message_useage < plan_info["Message_Limit"]:
                    best_plan.append(plan_info)

    min_cost = best_plan[0]["Plan_cost"]
    best_plan_ID = ""
    for plan_info in best_plan:
        if plan_info["Plan_cost"] < min_cost:
            min_cost = plan_info["Plan_cost"]
            best_plan_ID = plan_info["Plan_name"]

    return best_plan_ID




def pop_best_plan(phonenum, change_agency, use_c_agency):
    user_info = requests.get("http://127.0.0.1:8000/api/" + str(phonenum)) # 사용자 데이터
    user_info = user_info.json()

    norplan = requests.get("http://127.0.0.1:8000/norapi/") # 기본 요금제
    norplan = norplan.json()
    infplan = requests.get("http://127.0.0.1:8000/infapi/") # 무제한 요금제
    infplan = infplan.json()

    user_useage = requests.get("http://127.0.0.1:8000/useapi/" + str(phonenum))
    user_useage = user_useage.json()
    user_useage = user_useage[0]

    user_data = user_useage["Use_max"]# 사용자의 최대 데이터 사용량
    user_call = user_info["call_usage"] # 사용자의 전화 사용량
    user_message = user_info["message_usage"] # 사용자의 문자 사용량
    user_age = user_info["age"] # 사용자 나이

    # 사용자의 통신사
    user_plan_ID = user_info["Plan_ID"]
    if (user_plan_ID % 1000) // 100 == 0:
        user_plan = requests.get("http://127.0.0.1:8000/norapi/"+str(user_plan_ID))
        user_plan = user_plan.json()
        user_agency = user_plan["Agency_name"]
    else:
        user_plan = requests.get("http://127.0.0.1:8000/infapi/"+str(user_plan_ID))
        user_plan = user_plan.json()
        user_agency = user_plan["Agency_name"]

    best_plan = [] # 추천 가능한 모든 요금제

    # 통신사 변경 의사 = O
    if change_agency:
        # 사용자 가족의 통신사
        user_family = user_info["Family_ID"]
        user_family_info = requests.get("http://127.0.0.1:8000/familyapi/" + str(user_family))
        user_family_info = user_family_info.json()
        family_agency = user_family_info["agency_name"]

        # 사용자의 통신사와 가족의 통신사가 같은 경우 전체에서 추천
        if user_agency == family_agency:
            for plan_info in norplan:
                # 알뜰폰 요금제 사용하지 않을경우
                if not use_c_agency:
                    if plan_info["Plan_ID"] > 4000:
                        continue
                if plan_info["age"] == 65:
                    if user_age < 65:
                        continue
                elif plan_info["age"] == 18:
                    if user_age > 18:
                        continue
                elif plan_info["age"] == 24:
                    if (user_age < 19) or (user_age > 24):
                        continue

                if user_data < plan_info["Total_limit"]:
                    if user_call < plan_info["Call_Limit"]:
                        if user_message < plan_info["Message_Limit"]:
                            best_plan.append(plan_info)

            for plan_info in infplan:
                # 알뜰폰 요금제 사용하지 않을경우
                if not use_c_agency:
                    if plan_info["Plan_ID"] > 4000:
                        continue
                if plan_info["age"] == 65:
                    if user_age < 65:
                        continue
                elif plan_info["age"] == 18:
                    if user_age > 18:
                        continue
                elif plan_info["age"] == 24:
                    if (user_age < 19) or (user_age > 24):
                        continue
                if user_call < plan_info["Call_Limit"]:
                    if user_message < plan_info["Message_Limit"]:
                        best_plan.append(plan_info)

        # 사용자의 통신사와 가족의 통신사가 다른 경우 가족의 통신사로 추천
        else:
            for plan_info in norplan:
                # 알뜰폰 요금제 사용하지 않을경우
                if not use_c_agency:
                    if plan_info["Plan_ID"] > 4000:
                        continue
                if not (plan_info["Agency_name"] == family_agency):
                    continue
                if plan_info["age"] == 65:
                    if user_age < 65:
                        continue
                elif plan_info["age"] == 18:
                    if user_age > 18:
                        continue
                elif plan_info["age"] == 24:
                    if (user_age < 19) or (user_age > 24):
                        continue
                if user_data < plan_info["Total_limit"]:
                    if user_call < plan_info["Call_Limit"]:
                        if user_message < plan_info["Message_Limit"]:
                            best_plan.append(plan_info)

            for plan_info in infplan:
                # 알뜰폰 요금제 사용하지 않을경우
                if not use_c_agency:
                    if plan_info["Plan_ID"] > 4000:
                        continue
                if not (plan_info["Agency_name"] == family_agency):
                    continue
                if plan_info["age"] == 65:
                    if user_age < 65:
                        continue
                elif plan_info["age"] == 18:
                    if user_age > 18:
                        continue
                elif plan_info["age"] == 24:
                    if (user_age < 19) or (user_age > 24):
                        continue
                if user_call < plan_info["Call_Limit"]:
                    if user_message < plan_info["Message_Limit"]:
                        best_plan.append(plan_info)

    # 통신사 변경 의사 = X
    # 사용자의 통신사에서 추천
    else:
        for plan_info in norplan:
            # 알뜰폰 요금제 사용하지 않을경우
            if not use_c_agency:
                if plan_info["Plan_ID"] > 4000:
                    continue
            if not (plan_info["Agency_name"] == user_agency):
                continue
            if plan_info["age"] == 65:
                if user_age < 65:
                    continue
            elif plan_info["age"] == 18:
                if user_age > 18:
                    continue
            elif plan_info["age"] == 24:
                if (user_age < 19) or (user_age > 24):
                    continue
            if user_data < plan_info["Total_limit"]:
                if user_call < plan_info["Call_Limit"]:
                    if user_message < plan_info["Message_Limit"]:
                        best_plan.append(plan_info)

        for plan_info in infplan:
            # 알뜰폰 요금제 사용하지 않을경우
            if not use_c_agency:
                if plan_info["Plan_ID"] > 4000:
                    continue
            if not (plan_info["Agency_name"] == user_agency):
                continue
            if plan_info["age"] == 65:
                if user_age < 65:
                    continue
            elif plan_info["age"] == 18:
                if user_age > 18:
                    continue
            elif plan_info["age"] == 24:
                if (user_age < 19) or (user_age > 24):
                    continue
            if user_call < plan_info["Call_Limit"]:
                if user_message < plan_info["Message_Limit"]:
                    best_plan.append(plan_info)

    # 추천 가능한 모든 요금제 중에서 가장 저렴한 요금제 찾기
    min_cost = best_plan[0]["Plan_cost"]
    best_plan_ID = 0
    for plan_info in best_plan:
        if plan_info["Plan_cost"] < min_cost:
            min_cost = plan_info["Plan_cost"]
            best_plan_ID = plan_info["Plan_name"]

    return best_plan_ID