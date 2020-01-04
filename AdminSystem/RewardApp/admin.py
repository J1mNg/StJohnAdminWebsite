from django.contrib import admin
from .models import Reward, User_Reward_Log, Reward_Band

# Register your models here.
admin.site.register(Reward)
admin.site.register(User_Reward_Log)
admin.site.register(Reward_Band)