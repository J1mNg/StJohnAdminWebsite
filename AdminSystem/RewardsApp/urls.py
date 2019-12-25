from django.urls import path
from . import views


app_name='rewards'

urlpatterns = [
    path('', views.rewards_index, name="rewards"),
]
