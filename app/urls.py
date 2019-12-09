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

plan_list = views.PlanView.as_view({
    'get': 'list',
    'post': 'create'
})

plan_detail = views.PlanView.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})


agency_list = views.AgencyView.as_view({
    'get': 'list',
    'post': 'create'
})

agency_detail = views.AgencyView.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})

INF_list = views.InfdetailView.as_view({
    'get': 'list',
    'post': 'create'
})

INF_detail = views.InfdetailView.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})

Nor_list = views.NordetailView.as_view({
    'get': 'list',
    'post': 'create'
})

Nor_detail = views.NordetailView.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})
Family_list = views.FamilyView.as_view({
    'get': 'list',
    'post': 'create'
})

Family_detail = views.FamilyView.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'patch' : 'partial_update',
    'delete' : 'destroy'
})



urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', user_list, name='user_list'),
    path('api/<str:pk>/',user_detail, name='user_detail'),
    path('planapi/',plan_list, name='plan_list'),
    path('planapi/<int:pk>/',plan_detail,name='plan_detail'),
    path('agencyapi/', agency_list, name='agency_list'),
    path('agencyapi/<str:pk>',agency_detail, name='agency_detail'),
    path('norapi/', Nor_list, name='nor_list'),
    path('norapi/<int:pk>', Nor_detail, name='nor_detail'),
    path('infapi/',INF_list, name='inf_list'),
    path('infapi/<int:pk>', INF_detail, name='inf_detail'),
    path('familyapi/',Family_list, name='family_list'),
    path('familyapi/<int:pk>', Family_detail, name='family_detail'),

    path('makedata/',views.make_data, name="make_data"),
    path('make_agency_plan/', views.make_plan_agency_btn, name='make_agency_plan'),
    path('make_user/',views.make_user_btn,name='make_user'),
    path('make_family/',views.make_family_btn,name='make_family'),

    path('', views.index, name='index'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.signin, name='signin'),
    path('newuser/',views.newuserform, name ='newuserform')
    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
]