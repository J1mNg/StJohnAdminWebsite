from django.urls import path
from . import views


app_name='rollmarking'

urlpatterns = [
    path('', views.rollmarking_index, name="rollmarking"),
]
