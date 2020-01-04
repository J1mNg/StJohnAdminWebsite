"""AdminSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from RollMarkingApp import views

app_name='rollmarking'

urlpatterns = [
    path('', views.rollmarkingIndex, name='rollMarkingIndex'),
    path('addmeetings/', views.form_addmeetings, name="form_addmeetings"),
    path('view_attendance/<int:year>/term_<int:term>/', views.view_attendance, name="view_attendance"),
    path('mark_attendance/<int:year>/<int:month>/<int:day>', views.mark_attendance, name="mark_attendance"),
    path('add_attendance/', views.AttendanceCreateView.as_view(), name="add_attendance"),
]
