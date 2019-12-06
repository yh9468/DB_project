from rest_framework import serializers
from .models import MyUser, Plan, Family, Agency, INF_details, NOR_details          #아마도 각 class마다 시리얼라이저를 처리해줘야 할것같다.

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ('Agency_name', 'Agency_phone')
        exclude = ()

class FamilySerializer(serializers.ModelSerializer):
    agency = AgencySerializer(read_only=True)
    class Meta:
        model = Family
        fields = ('Family_id', 'agency_name')
        exclude = ()

class PlanSerializer(serializers.ModelSerializer):
    agency = AgencySerializer(read_only=True)
    class Meta:
        model = Plan
        fields = ('Plan_name', 'Call_Limit', 'Message_Limit', 'Agency_name')
        exclude = ()

class InfdetailSerializer(serializers.ModelSerializer):
    agency = AgencySerializer(read_only=True)
    class Meta:
        model = INF_details
        fields = ('Plan_name', 'Call_Limit', 'Message_Limit', 'Agency_name'
                  ,'Month_limit', 'Day_limit')
        exclude = ()

class NordetailSerializer(serializers.ModelSerializer):
    agency = AgencySerializer(read_only=True)
    class Meta:
        model = NOR_details
        fields = ('Plan_name', 'Call_Limit', 'Message_Limit', 'Agency_name', 'Total_limit')
        exclude = ()

class MyUserSerializer(serializers.ModelSerializer):
    family = FamilySerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = MyUser
        field=('phonenum', 'password', 'name', 'data_usage','message_usage',
               'call_usage', 'user_contents', 'family_number', 'plan_name')
        exclude = ('password','user_permissions','groups','is_superuser', 'last_login',)     #api 에서 제공되는 것을 제거하는것.
