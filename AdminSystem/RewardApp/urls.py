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
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import admin
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from RewardApp import views

admin.autodiscover()

app_name='rewards'

urlpatterns = [
    path('', views.rewards_index_view.as_view(), name='reward_index'),
    path('allRewards/', views.all_rewards_view.as_view(), name='all_rewards_view'),
    path('rewardTier/', views.reward_tier_view.as_view(), name='reward_tier_view'),
    path('adminReward/', views.admin_reward_view, name='admin_reward_view'),
    path('confirm_reward/<int:cadet_id>/<int:reward_tier>/', views.confirm_reward_view, name="confirm_reward_view"),
    path('cadetReward/', views.rewards_cadets_list_view, name="cadet_reward_list_view"),
    path('cadetReward/detailView/<int:cadet_id>/', views.cadet_reward_detail_view, name="cadet_reward_detail_view"),
    path('updateRewards/', views.update_rewards_csv_view, name="update_db_index_view"),
    path('updateDB/<str:data_type>/', views.update_db_view, name="update_db"),
]