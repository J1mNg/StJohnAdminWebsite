from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db.models import ObjectDoesNotExist, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db import models
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models.base import ObjectDoesNotExist

import datetime
import csv
import io

from CadetApp.models import Cadet
from RewardApp.models import Reward, User_Reward_Log, Reward_Band

# Factory classes
class RewardTierFactory():
    def create_reward_band(self, tier, req_hrs):
        reward_tier = Reward_Band(reward_band = tier, required_hours = req_hrs)

        return reward_tier

class RewardItemFactory():
    def create_reward_item(self, name, cost, req_pts, source, link, comments="", isActive=False):
        reward = Reward(name=name, price=cost, required_points=req_pts, source=source, link=link, comments=comments, IsActive=isActive)

        return reward

# Helper Functions
def check_admin(user):
   return user.is_superuser

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
        cadets = Cadet.objects.filter(is_active=True)
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

@user_passes_test(check_admin)
def admin_reward_view(request):
    cadets = Cadet.objects.all().filter(is_active=True)
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
    cadets = Cadet.objects.all().filter(is_active=True)

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

@user_passes_test(check_admin)
def update_rewards_csv_view(request):
    template_name = "update_db_form.html"

    return render(request, template_name)

@user_passes_test(check_admin)
def update_db_view(request, data_type):
    if request.method == 'GET':
        return redirect('/rewards/updateRewards/')

    try:
        io_string = get_io_string(request, data_type)

        reader = csv.reader(io_string, delimiter=",", quotechar='"')
        next(reader, None) # skips CSV headers

        if data_type == "allRewards":
            Reward.objects.all().delete()
            reward_name = reward_type = reward_source = reward_cost = reward_band = reward_link = reward_comments = ""
            reward_isActive = False

            reward_item_factory = RewardItemFactory()

            for column in reader:
                try:
                    reward_name = column[0],
                    reward_source = column[2],
                    reward_cost = column[3],
                    reward_band = column[4],
                    reward_link = column[7],

                    try:
                        reward_band = int(reward_band[0])
                        reward_isActive = True
                        reward_req_pts_obj = Reward_Band.objects.get(reward_band = reward_band)
                    except ValueError: # If band is empty, reward is Inactive
                        reward_req_pts_obj = Reward_Band.objects.get(reward_band = 0)
                        reward_band = 0
                        reward_isActive = False
                    except Reward_Band.DoesNotExist:
                        messages.warning(request, 'Failed to update database. Ensure correctness of file being submitted. (Columns)')
                        break

                    # Create Obj and Save
                    reward_item_obj = reward_item_factory.create_reward_item(reward_name[0], reward_cost[0], reward_req_pts_obj, reward_source[0], reward_link[0], reward_comments, reward_isActive)
                    
                    try:
                        reward_item_obj.save()
                    except ValueError:
                        messages.warning(request, 'Failed to update database. Please try again.')
                        pass
                except IndexError:
                    messages.warning(request, 'Failed to update database. Ensure correctness of file being submitted. (Columns)')
                    break
                except Reward_Band.DoesNotExist:
                    messages.warning(request, 'Failed to update database. Ensure Reward Tier Database exists. Try Updating "Reward Tier Database" first and try again.')
                    break

            if len(list(messages.get_messages(request))) == 0:
                messages.success(request, 'All Rewards Database has successfully been updated. Please go to admin dashboard to confirm successfull update.')

        elif data_type == "rewardTier":
            Reward_Band.objects.all().delete() # Delete current reward band database
            reward_tier = reward_required_hours = "" # Init variables
            reward_tier_factory = RewardTierFactory() 

            try: 
                if Reward.objects.all().count() == 0:
                    messages.warning(request, 'Database updated. But Rewards database does not exist. Please Create a Rewards Database and update Rewards Tier again.')
            except TypeError:
                pass

            for column in reader: # For each entry in database, create a reward tier object, and make an entry into db
                reward_tier = column[0]
                reward_required_hours = column[1]

                # Create obj and save
                reward_tier_obj = reward_tier_factory.create_reward_band(reward_tier, reward_required_hours)

                try:
                    reward_tier_obj.save()
                    
                    try:
                        for i in range(2, 10):
                            reward_name = column[i]
                            if reward_name not in (None, ""):
                                try:
                                    reward_obj = Reward.objects.get(name=reward_name)
                                    reward_tier_obj.rewards_list.add(reward_obj)
                                    reward_tier_obj.save()
                                except Reward.DoesNotExist:
                                    break
                    except IndexError:        
                        pass
                except ValueError:
                    messages.warning(request, 'Database has failed to update. Please check the file columns to ensure that they are in correct format')
                    break
            
            if len(list(messages.get_messages(request))) == 0:
                messages.success(request, 'Reward Tier Database has successfully been updated. Please go to admin dashboard to configure individual rewards for each tier.')
    
    except MultiValueDictKeyError:
        messages.warning(request, 'Failed to update database. Please try again.')

    # Redirect to upload page upon completion with message
    return redirect('/rewards/updateRewards/')

def get_io_string(request, data_type):
    if data_type == "allRewards":
        csv_file = request.FILES['file_rewards_all']
    elif data_type == "rewardTier":
        csv_file = request.FILES['file_rewards_tier']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please upload a .csv file.')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    
    return io_string