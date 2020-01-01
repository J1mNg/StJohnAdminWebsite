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

        cadets_list = list(cadets)

        for cadet in cadets_list:
            for tier in reward_tier:
                if tier.reward_band > 0:
                    if not (0 < (cadet.total_duty_hours - tier.required_hours) <= 5):
                        cadets_list.remove(cadet)
                        break;

        queryset = {'cadets': cadets}

        return queryset

    # class TermFeeListView(ListView):
    # template_name = 'FinancesApp/termfee_view.html'
    # # returns queryset called 'all_cadets'
    # context_object_name = 'all_cadets'

    # #kwargs --> the values we pass into URL
    # def get_queryset(self):
    #     # get all objects in TermFee with a meeting whose term and date__year is the same as the one passed into urls
    #     # date__year --> gets the year from a date field
    #     paid = TermFee.objects.filter(meeting__term=self.kwargs['term'], meeting__date__year=self.kwargs['year'])
    #     # paid.values('cadet') --> returns a list of dictionaries --> [{'cadet':pk_1}, {'cadet':pk_2} ...]
    #     # exclude all cadet objects with a primary key in the query set of paid.values('cadet')
    #     not_paid = Cadet.objects.exclude(user_id__in=paid.values('cadet'))
    #     # partition the query set
    #     queryset = {'paid':paid, 'not_paid':not_paid}
    #     return queryset