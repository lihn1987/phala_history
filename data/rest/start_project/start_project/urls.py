"""start_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from start_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/get_top10_owner', views.get_top10_owner),
    path('rest/get_top10_staker', views.get_top10_staker),
    path('rest/get_param', views.get_param),
    path('rest/get_latest_daily_v', views.get_latest_daily_v),
    path('rest/get_latest_daily_stake', views.get_latest_daily_stake),
    path('rest/get_latest_daily_mechine_count', views.get_latest_daily_mechine_count),
    path('rest/get_latest_daily_mechine_user_count', views.get_latest_daily_mechine_user_count),
    path('rest/get_mechines/<str:pid>/<str:status>/<str:pubkey>/<int:page>', views.get_mechines),
    path('rest/get_bml_error_pid', views.get_bml_error_pid),
    path('rest/get_bml_special_error_mechine', views.get_bml_special_error_mechine),
    path('rest/get_bml_error_mechine', views.get_bml_error_mechine),
    path('rest/get_bml_xq', views.get_bml_xq),
]
