from django.shortcuts import render

# Create your views here.

def rewards_index(request):
    return render(request, "RewardsApp/rewards_base.html")
