from django.contrib import admin
from .models import Meeting, Attendance, Absence

# Register your models here.

admin.site.register(Meeting)
admin.site.register(Attendance)
admin.site.register(Absence)
