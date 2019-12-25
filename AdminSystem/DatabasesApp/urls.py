from django.urls import path
from . import views


app_name='viewdatabases'

urlpatterns = [
    path('', views.databases_index, name="viewdatabases"),
]
