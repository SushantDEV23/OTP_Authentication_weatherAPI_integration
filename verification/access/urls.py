from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns=[
    path('', home, name='home'),
    path('login_attempt', login_attempt, name='login_attempt'),
    path('register', register, name='register'),
    path('otp', otp, name='otp'),
    path('weather', weather, name='weather'),
    path('login_otp', login_otp, name='login_otp')
]