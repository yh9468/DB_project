from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


user_list = views.MyUserView.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = views.MyUserView.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', user_list, name='user_list'),
    path('api/<str:pk>/',user_detail, name='user_detail'),
    path('makedata/',views.make_data, name="make_data"),

    path('selectleft/', views.testleft, name='test_left'),
    path('selectright/',views.testright,name='test_right'),

    path('', views.index, name='index'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.signin, name='signin'),
    path('newuser/',views.newuserform, name ='newuserform')
    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
]