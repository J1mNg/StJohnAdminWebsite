from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db import models

import datetime

from CadetApp.models import Cadet
from RewardApp.models import Reward, User_Reward_Log, Reward_Band

# Helper Functions
def check_received_rewards(cadet, reward_tier):
    """[checks if given reward has recieved the reward for the given reward tier]

    Arguments:
        cadet {[Cadet]} -- [cadet object]
        reward_tier {[int]} -- [reward tier]

    Return:
        boolean
    """

    if User_Reward_Log.objects.filter(cadet=cadet, reward_tier=reward_tier).exists():
        return True
    else:
        return False

def rewardListToString(s):
    """[Turns a List of Reward Objects into a comma seperated strings]

    Arguments:
        s {[list of rewards]} -- [list of rewards]

    Returns:
        [String] -- [string of comma seperated reward names]
    """

    # initialize an empty string
    str1 = ""
    reward_list = []

    # traverse in the string
    for ele in s:
        reward_list.append(ele.name)

    str1 = ", ".join(reward_list)

    # return string
    return str1

def rewardListToListOfRewardName(s):
    str1 = ""
    reward_list = []

    # traverse in the string
    for ele in s:
        reward_list.append(ele.name)

    str1 = ", ".join(reward_list)

    reward_list = str1.split(",")

    return reward_list

# Create your views here.
class rewards_index_view(ListView):
    template_name="reward_index.html"

    def get_queryset(self):
        """[Returns 2 query sets, including list of cadets who are about to achieve
        next milestone, and list of cadets who have achieved their milestone, but has
        yet to recieve their reward from the admin]

        Returns:
            [queryset] -- [dictionary of defined querysets]
        """
        cadets = Cadet.objects.all()
        reward_log = User_Reward_Log.objects.all()
        rewards = Reward.objects.all()
        reward_tier = Reward_Band.objects.all()

        # cadets who are close to reaching their next milestone
        cadets_list = []
        # cadets who have achieved their milestone, but have yet to recieve their reward
        cadets_need_to_get_reward_list = []

        for cadet in cadets:
            for tier in reward_tier:
                if tier.reward_band > 0:
                    if cadet.total_duty_hours < tier.required_hours:
                        if cadet.total_duty_hours + 5 >= tier.required_hours:
                            cadet_info = {
                                'name': cadet.firstname + " " + cadet.lastname,
                                'pts_needed': abs(cadet.total_duty_hours - tier.required_hours),
                                'current_hours': cadet.total_duty_hours,
                                'tier_to_be_reached': tier.reward_band,
                            }
                            cadets_list.append(cadet_info)
                            break

        for cadet in cadets:
            for tier in reward_tier:
                if tier.reward_band > 0:
                    if cadet.total_duty_hours > tier.required_hours:
                        if not (check_received_rewards(cadet, tier.reward_band)):
                            rewards_list = []
                            for reward in tier.rewards_list.all():
                                rewards_list.append(reward)

                            cadet_info = {
                                'name': cadet.firstname + " " + cadet.lastname,
                                'tier': tier.reward_band,
                                'rewards': rewardListToListOfRewardName(rewards_list)
                            }
                            cadets_need_to_get_reward_list.append(cadet_info)


        queryset = {'cadets': cadets_list, 'cadets_get_reward': cadets_need_to_get_reward_list}

        return queryset

class all_rewards_view(ListView):
    login_required = True
    template_name = "all_rewards.html"

    def get_queryset(self):
        rewards = Reward.objects.all()

        queryset = {'rewards': rewards}

        return queryset

class reward_tier_view(ListView):
    template_name = "reward_tier_view.html"

    def get_queryset(self):
        tiers = Reward_Band.objects.all()

        reward_information_list = []

        for tier in tiers:
            if tier.reward_band > 0:
                rewards_list = []
                for reward in tier.rewards_list.all():
                    rewards_list.append(reward)

                reward_info = {
                    'reward_band': tier.reward_band,
                    'required_hours': tier.required_hours,
                    'rewards': rewardListToString(rewards_list)
                }

                reward_information_list.append(reward_info)

        queryset = {'rewards': reward_information_list}

        return queryset

def admin_reward_view(request):
    cadets = Cadet.objects.all()
    reward_log = User_Reward_Log.objects.all()
    rewards = Reward.objects.all()
    reward_tier = Reward_Band.objects.all()

    cadets_need_to_get_reward_list = []

    for cadet in cadets:
        for tier in reward_tier:
            if tier.reward_band > 0:
                if cadet.total_duty_hours > tier.required_hours:
                    if not (check_received_rewards(cadet, tier.reward_band)):
                        cadet_info = {
                            'pk': cadet.user_id,
                            'name': cadet.firstname + " " + cadet.lastname,
                            'tier': tier.reward_band,
                            'rewards': tier.rewards_list.all(),
                        }

                        cadets_need_to_get_reward_list.append(cadet_info)


    queryset = {'cadets_get_reward': cadets_need_to_get_reward_list}

    return render(request, "admin_rewards.html", queryset)

class LogManager(models.Manager):
    def create_reward_log_entry(self, cadet, rewards_tier, reward, reward_claim_date):
        reward_log_entry = self.create(cadet=cadet, reward_tier=rewards_tier, reward=reward, reward_claim_date=reward_claim_date)
        # do something with the book
        return reward_log_entry

def confirm_reward_view(request, cadet_id, reward_tier):
    if request.method == 'POST':
        if 'Confirm Reward' in request.POST.values():
            selected_reward = request.POST.getlist('reward', None)
            selected_reward = selected_reward[0]
            curr_date = datetime.date.today()
            cadet_obj =  Cadet.objects.get(pk=cadet_id)
            reward_obj = Reward.objects.get(name=selected_reward)

            log_entry = User_Reward_Log(cadet=cadet_obj, reward_tier=reward_tier, reward=reward_obj, reward_claim_date=curr_date)

            log_entry.save()

            return redirect('/rewards/adminReward/')


    return redirect('/rewards/adminReward/')

def rewards_cadets_list_view(request):
    cadets = Cadet.objects.all()

    queryset = {'cadets': cadets}

    return render(request, "reward_cadets_list.html", queryset)

def cadet_reward_detail_view(request, cadet_id):
    cadet_obj = Cadet.objects.get(pk=cadet_id)

    reward_log_obj = User_Reward_Log.objects.filter(cadet=cadet_obj)

    queryset = {'reward_logs': reward_log_obj}

    if len(reward_log_obj) == 0:
        messages.info(request, 'The selected cadet has not claimed any rewards yet!')

        return redirect("/rewards/cadetReward/")
    else:
        return render(request, "cadet_reward_detail_view.html", queryset)
