"""
URL configuration for web_project_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from webproject_back import views, urls

urlpatterns = [
    path('admin/register-users', views.register_users),
    path('admin/list-users', views.list_users),
    path('admin/register-item', views.register_item),
    path('admin/list-itens', views.list_itens),
    path('admin/register-user-item', views.register_user_item),
    path('admin/list-user-itens', views.list_user_itens),
    path('admin/excel/generate', views.generate_excel)
]
