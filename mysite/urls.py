"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.conf.urls import include
from django.urls import re_path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    # path('',views.base,name ='base'),
    path('', views.index),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    re_path(r'^captcha/', include('captcha.urls'), name='captchas'),  # 添加captcha相对应的网址
    re_path(r'^confirm/$', views.user_confirm, name='cofirms')
]
