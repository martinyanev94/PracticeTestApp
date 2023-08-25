from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from payment.models import UserMembership


@login_required(login_url='/authentication/login')
# Create your views here.
def payment_plans(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()

    context = {
        'user_membership': user_membership.membership,

    }

    return render(request, 'payment/payment_plans.html', context)
