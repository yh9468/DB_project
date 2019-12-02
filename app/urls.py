from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('login/', views.signin, name='signin'),
    path('newuser/',views.newuserform, name ='newuserform')
    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
]