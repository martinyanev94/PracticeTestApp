from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='/authentication/login')
# Create your views here.
def payment_plans(request):
    return render(request, 'payment/payment_plans.html')