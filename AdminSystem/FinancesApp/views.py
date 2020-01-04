from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .models import TermFee, Expense
from RollMarkingApp.models import Meeting
from CadetApp.models import Cadet

from .forms import IndexRedirectForm

import datetime
# Create your views here.

### Not finished
def financesIndex(request):
    now = datetime.datetime.now()

    if request.method == 'POST':
        get_request = request.POST
        form = IndexRedirectForm(get_request, initial={'year': now.year})
        if form.is_valid():
            data = form.cleaned_data
            if 'view_year_finances' in get_request:
                return redirect('finances:view-finances', year=data['year'], term=0, month=0)
            elif 'view_term_finances' in get_request:
                return redirect('finances:view-finances', year=data['year'], term=data['term_finances'], month=0)
            elif 'view_month_finances' in get_request:
                return redirect('finances:view-finances', year=data['year'], term=0, month=data['month'])
            elif 'view_term_termfees' in get_request:
                return redirect('finances:termfee-list', year=data['year'], term=data['term_termfees'])
    else:
        #initial doesn't work
        form = IndexRedirectForm(initial={'year': now.year})

    return render(request, 'FinancesApp/finances_index.html', {'form': form})

class FinancesListView(ListView):
    template_name = 'FinancesApp/viewfinances_term.html'
    context_object_name = 'all_finances'

    def get_queryset(self):
        meetings=[]
        if self.kwargs['month'] == 0 and self.kwargs['term'] == 0:
            meetings = Meeting.objects.all()
        elif self.kwargs['month'] == 0:
            meetings = Meeting.objects.filter(term=self.kwargs['term'])
        elif self.kwargs['term'] == 0:
            meetings = Meeting.objects.filter(date__month=self.kwargs['month'])
        queryset = {'meetings':meetings}
        return queryset


# CreateView --> creates a row in the table (TermFees)
# different to FormView --> for displaying a form

###success message wrapped in green
class TermFeeCreateView(SuccessMessageMixin, CreateView):
    model = TermFee
    template_name = 'FinancesApp/termfee_form.html'
    initial = {'amount': '20'}
    fields = '__all__'
    # redirect URL --> app name:view name
    success_url = reverse_lazy('finances:termfee-create')
    success_message = "%(cadet)s term fee payment successfully entered"

# ListView --> iterates over all the objects of a model for displaying purposes
# Suppose we want to filter these objects --> we have to redefine get_queryset (the queryset that ListView returns)

### column for when they paid
class TermFeeListView(ListView):
    template_name = 'FinancesApp/termfee_view.html'
    # returns queryset called 'all_cadets'
    context_object_name = 'all_cadets'

    #kwargs --> the values we pass into URL
    def get_queryset(self):
        # get all objects in TermFee with a meeting whose term and date__year is the same as the one passed into urls
        # date__year --> gets the year from a date field
        paid = TermFee.objects.filter(meeting__term=self.kwargs['term'], meeting__date__year=self.kwargs['year'])
        # paid.values('cadet') --> returns a list of dictionaries --> [{'cadet':pk_1}, {'cadet':pk_2} ...]
        # exclude all cadet objects with a primary key in the query set of paid.values('cadet')
        not_paid = Cadet.objects.exclude(user_id__in=paid.values('cadet'))
        # partition the query set
        queryset = {'paid':paid, 'not_paid':not_paid}
        return queryset

class TermFeeDeleteView(DeleteView):
    model = TermFee
    success_url = reverse_lazy('finances:finances_index')


class ExpenseCreateView(SuccessMessageMixin, CreateView):
    model = Expense
    template_name = 'FinancesApp/expense_form.html'
    fields = '__all__'
    # redirect URL --> app name:view name
    success_url = reverse_lazy('finances:expense-create')
    success_message = "%(cadet)s has an expense of %(amount)s"
