from django.shortcuts import render

# Create your views here.
def payment_plans(request):
    return render(request, 'payment/payment_plans.html')