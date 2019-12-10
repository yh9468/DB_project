from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django import forms
import json

class MyUserManager(BaseUserManager):
    def create_user(self, phonenum, name ,password=None):
        if not phonenum:
            raise ValueError('폰번호는 필수입니다.')
        user = self.model(phonenum=phonenum, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phonenum, name , password):
        user = self.create_user(
            phonenum=phonenum,
            password=password,
            name=name
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):
    phonenum = models.CharField(primary_key=True, max_length=20)    #PK
    name = models.CharField(max_length=10)      #이름
    Plan_ID = models.ForeignKey(
        'Plan',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    Family_ID = models.ForeignKey(
        'Family',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    age = models.PositiveIntegerField("age", null=False)
    message_usage = models.PositiveIntegerField("message_usage", null=False, default=0)    #메시지 사용량
    call_usage = models.PositiveIntegerField("call_usage", null=False, default=0)       #전화 사용량

    User_contents = models.CharField(max_length=10)
    # Family_number = models.ForeignKey(
    #     'Family',
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True
    # ) 가족이 FK로 유저의 phone num을 참조하는게 맞을것같습니다.

    USERNAME_FIELD = 'phonenum'
    REQUIRED_FIELDS = ['name', 'Plan_name', 'message_usage', 'call_usage']
    objects = MyUserManager()

    class Meta:
        db_table = 'User_table'
        verbose_name = '유저'
        verbose_name_plural = '유저들'

    #클래스를 어떻게 표현할 것인지에 대해서
    def __str__(self):
        return self.phonenum

    def get_full_name(self):
        return self.phonenum

    def get_short_name(self):
        return self.phonenum

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

class Use_detail(models.Model):
    phonenum = models.ForeignKey(
        'MyUser',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    Jan = models.FloatField("Jan", null=False)
    Feb = models.FloatField("Feb", null=False)
    Mar = models.FloatField("Mar", null=False)
    Apr = models.FloatField("Apr", null=False)
    May = models.FloatField("May", null=False)
    Jun = models.FloatField("Jun", null=False)
    Jul = models.FloatField("Jul", null=False)
    Aug = models.FloatField("Aug", null=False)
    Sep = models.FloatField("Sep", null=False)
    Oct = models.FloatField("Oct", null=False)
    Nov = models.FloatField("Nov", null=False)
    Dec = models.FloatField("Dec", null=False)
    Use_max = models.FloatField('Use_max', null=False)

    class Meta:
        db_table = 'Use_table'
        verbose_name="사용량"

def JSON_to_MyUser(json_str):
    # dict = json.loads(json_str)
    dict = json_str
    myuser = MyUser()

    myuser.phonenum = dict['phonenum']
    myuser.name = dict['name']
    myuser.message_usage = dict['message_usage']
    myuser.call_usage = dict['call_usage']
    myuser.User_contents = dict["User_contents"]
    myuser.Plan_ID = Plan.objects.get(pk=dict['Plan_ID'])
    myuser.Family_ID = Family.objects.get(pk=dict['Family_ID'])
    myuser.age = dict['age']
    return myuser

def JSON_to_use(json_str):
    dict = json_str[0]
    myuse = Use_detail()
    myuse.id = dict['id']
    myuse.phonenum = MyUser.objects.get(pk=dict['phonenum'])
    myuse.Jan = dict['Jan']
    myuse.Feb = dict['Feb']
    myuse.Mar = dict['Mar']
    myuse.Apr = dict['Apr']
    myuse.May = dict['May']
    myuse.Jun = dict['Jun']
    myuse.Jul = dict['Jul']
    myuse.Aug = dict['Aug']
    myuse.Sep = dict['Sep']
    myuse.Oct = dict['Oct']
    myuse.Nov = dict['Nov']
    myuse.Dec = dict['Dec']
    myuse.Use_max = dict['Use_max']
    return myuse

class NewUser:
    def __init__(self,phonenum, name, age, main_content, data_usage, Agency_name, Check_INF):
        self.phonenum = phonenum
        self.name = name
        self.age = age
        self.main_content = main_content
        self.data_usage = data_usage
        self.Agency_name = Agency_name
        self.Check_INF = Check_INF

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def JSON_To_NewUser(json_str):
    dict = json.loads(json_str)
    phonenum = dict['phonenum']
    name = dict['name']
    age = dict['age']
    main_content = dict['main_content']
    data_usage = dict['data_usage']
    Agency_name = dict['Agency_name']
    Check_INF = dict['Check_INF']
    return NewUser(phonenum, name, age, main_content, data_usage,Agency_name,Check_INF)


#가족 엔티티
class Family(models.Model):
    Family_id = models.IntegerField("Family_id", primary_key=True, null=False)
    agency_name = models.ForeignKey(
        'Agency',
        models.SET_NULL,
        blank=True,
        null=True,
    )
    class Meta:
        db_table = 'Family_table'
        verbose_name = '가족'
        verbose_name_plural = '가족들'

#통신사 엔티티
class Agency(models.Model):
    Agency_name = models.CharField(max_length=10, primary_key=True, null=False)
    Agency_phone = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'Agency_table'

    def __str__(self):
        return self.Agency_name

class Plan(models.Model):
    Plan_cost = models.PositiveIntegerField("Plan_cost", null=False)
    Plan_name = models.CharField(max_length=50, null=False)
    Plan_ID = models.PositiveIntegerField("Plan_ID", null=False, primary_key=True)
    age =models.PositiveIntegerField('age', null=False)
    Agency_name = models.ForeignKey(
        'Agency',
        on_delete=models.CASCADE,           #통신사 사라지면 요금제도 당연히 사라져야 하므로
        null=False,
        blank=False
    )
    Call_Limit = models.PositiveIntegerField("Call_Limit", null=False)       #unsigned
    Message_Limit = models.PositiveIntegerField("Message_Limit", null=False)
    class Meta:
        db_table = 'Plan_table'
        verbose_name = '요금제'
        verbose_name_plural = '요금제들'
    def __str__(self):
        return self.Plan_name

class INF_details(Plan):
    Month_limit = models.FloatField("Month_limit", null=False)
    Day_limit = models.FloatField("Day_limit", null=False)

    class Meta:
        db_table = 'INF_table'

class NOR_details(Plan):
    Total_limit = models.FloatField("Total_limit", null=False)

    class Meta:
        db_table = 'NOR_table'


class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['phonenum']
