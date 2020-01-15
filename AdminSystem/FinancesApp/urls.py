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
from django.contrib import admin
from django.urls import path
from FinancesApp import views

app_name='finances'

urlpatterns = [
    path('', views.financesIndex, name='finances_index'),
    path('view_finances/<int:year>/term_<int:term>/month_<int:month>/', views.FinancesListView.as_view(), name='view-finances'),
    path('view_termfees/<int:year>/term_<int:term>/', views.TermFeeListView.as_view(), name='termfee-list'),
    path('pay_termfees/', views.TermFeeCreateView.as_view(), name='termfee-create'),
    path('delete_termfees/<int:pk>/', views.TermFeeDeleteView.as_view(), name='termfee-delete'),
    path('add_expenses/', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('add_otherincome/', views.OtherIncomeCreateView.as_view(), name='otherincome-create'),
    path('reconciliate_cashbox/', views.CashboxCreateView.as_view(), name='cashbox-create'),    
]
