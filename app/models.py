from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django import forms


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
            name= name
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):
    phonenum = models.CharField(primary_key=True, max_length=20)    #PK
    name = models.CharField(max_length=10)      #이름
    Agency_name = models.ForeignKey(
        'Agency',
        models.SET_NULL,
        blank=True,
        null=True
    )
    Plan_name = models.ForeignKey(
        'Plan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    data_useage = models.TextField()            #데이터 사용량
    message_useage = models.PositiveIntegerField(10, null=False, default=0)    #메시지 사용량
    call_useage = models.PositiveIntegerField(10, null=False, default=0)       #전화 사용량

    User_contents = models.CharField(max_length=10)
    Family_number = models.ForeignKey(
        'Family',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'phonenum'
    REQUIRED_FIELDS = ['name']
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

#가족 엔티티
class Family(models.Model):
    Family_id = models.IntegerField(10, primary_key=True, null=False)
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
    
    def __str__(self):
        return self.Family_id

#통신사 엔티티
class Agency(models.Model):
    Agency_name = models.CharField(max_length=30, primary_key=True, null=False)
    Agency_phone = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'Agency_table'

    def __str__(self):
        return self.Agency_name

class Plan(models.Model):
    Plan_name = models.CharField(max_length=20, null=False,primary_key=True)
    Agency_name = models.ForeignKey(
        'Agency',
        on_delete=models.CASCADE,           #통신사 사라지면 요금제도 당연히 사라져야 하므로
        null=False,
        blank=False
    )
    Call_Limit = models.PositiveIntegerField(10, null=False)       #unsigned
    Message_Limit = models.PositiveIntegerField(10, null=False)
    class Meta:
        db_table = 'Plan_table'
        verbose_name = '요금제'
        verbose_name_plural = '요금제들'

class INF_details(Plan):
    Month_limit = models.PositiveIntegerField(10, null=False)
    Day_limit = models.PositiveIntegerField(10, null=False)

    class Meta:
        db_table = 'INF_table'

class NOR_details(Plan):
    Total_limit = models.PositiveIntegerField(10, null=False)

    class Meta:
        db_table = 'NOR_table'


class LoginForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['phonenum']
