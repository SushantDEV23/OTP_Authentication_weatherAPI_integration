from django.contrib import admin
from django.urls import path
from access.views import register, home, login_attempt, login_otp, otp, weather
urlpatterns=[
    path('', home, name='home'),
    path('login_attempt/', login_attempt, name='login'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('weather/', weather, name='weather'),
    path('login_otp/', login_otp, name='login_otp')
]