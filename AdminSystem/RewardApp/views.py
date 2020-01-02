from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from CadetApp.models import Cadet
from RewardApp.models import Reward, User_Reward_Log, Reward_Band

# Create your views here.
class rewards_index_view(ListView):
    template_name="reward_index.html"

    def get_queryset(self):
        cadets = Cadet.objects.all()
        reward_log = User_Reward_Log.objects.all()
        rewards = Reward.objects.all()
        reward_tier = Reward_Band.objects.all()

        cadets_list = []
        cadets_need_to_get_reward_list = []

        for cadet in cadets:
            for tier in reward_tier:
                if tier.reward_band > 0:
                    if (0 < abs(cadet.total_duty_hours - tier.required_hours) <= 5):
                        cadet_info = {
                            'name': cadet.firstname + " " + cadet.lastname,
                            'pts_needed': abs(cadet.total_duty_hours - tier.required_hours),
                            'current_hours': cadet.total_duty_hours,
                            'tier_to_be_reached': tier.reward_band,
                        }
                        cadets_list.append(cadet_info)
                        break

        queryset = {'cadets': cadets_list, 'cadets_get_reward': cadets_need_to_get_reward_list}

        return queryset