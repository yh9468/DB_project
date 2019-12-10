from rest_framework import serializers
from .models import MyUser, Plan, Family, Agency, INF_details, NOR_details, Use_detail           #아마도 각 class마다 시리얼라이저를 처리해줘야 할것같다.


class InfdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = INF_details
        fields = ('Plan_name', 'Call_Limit', 'Message_Limit', 'Agency_name', 'Plan_cost', 'Plan_ID','age'
                  ,'Month_limit', 'Day_limit')
        exclude = ()

class NordetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NOR_details
        fields = ('Plan_name', 'Call_Limit', 'Message_Limit', 'Agency_name', 'Total_limit', 'Plan_cost', 'Plan_ID', 'age')
        exclude = ()


class UseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Use_detail
        field=('phonenum', 'Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep', 'Oct','Nov', 'Dec', 'Use_max')
        exclude = ()


class MyUserSerializer(serializers.ModelSerializer):
    use = UseSerializer(many=False, read_only=True)                              #한사람당 하나씩 이니까 one to one
    class Meta:
        model = MyUser
        field=('phonenum', 'password', 'name','message_usage',
               'call_usage', 'User_contents', 'Family_ID', 'Plan_ID', 'age', 'use')
        exclude = ('user_permissions','groups','is_superuser', 'last_login',)     #api 에서 제공되는 것을 제거하는것.

class FamilySerializer(serializers.ModelSerializer):
    myuser = MyUserSerializer(many=True, read_only=True)
    class Meta:
        model = Family
        fields = ('Family_id', 'agency_name', 'myuser')
        exclude = ()


class PlanSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(many=True, read_only=True)
    class Meta:
        model = Plan
        fields = ('Plan_name', 'Call_Limit', 'Message_Limit', 'Agency_name', 'Plan_cost', 'Plan_ID' , 'user', 'age')
        exclude = ()


class AgencySerializer(serializers.ModelSerializer):
    plan = PlanSerializer(many=True, read_only=True)
    family = FamilySerializer(many=True, read_only=True)
    class Meta:
        model = Agency
        fields = ('Agency_name', 'Agency_phone','plan','family')
        exclude = ()

