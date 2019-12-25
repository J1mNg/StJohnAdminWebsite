from django.shortcuts import render

# Create your views here.

def rollmarking_index(request):
    return render(request, "RollMarkingApp/rollMarking_base.html")
