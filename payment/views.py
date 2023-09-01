from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.templatetags.static import static
from django.views import View

from payment.models import UserMembership


@login_required(login_url='/authentication/login')
# Create your views here.
def payment_plans(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()

    context = {
        'user_membership': user_membership.membership,

    }

    return render(request, 'payment/payment_plans.html', context)


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.urls import reverse

from .models import Membership, UserMembership, Subscription

import stripe


def manage_membership(request):
    user_membership = UserMembership.objects.filter(user=request.user).first()
    user_stripe_subscription = get_stripe_subscriptions(user_membership.stripe_customer_id)

    # If there is a subscription and it is active
    if user_stripe_subscription:
        stripe_membership = Membership.objects.filter(stripe_plan_id=user_stripe_subscription[0].plan.id).first()

        # if stripe subscription is active ensure local membership and subscription are up-to-date
        if user_stripe_subscription[0].plan.active:

            # If local membership is not same as stripe membership: local=stripe and update subscription id
            if stripe_membership.membership_type != user_membership.membership:
                user_membership.membership = stripe_membership
                user_membership.save()

                sub, created = Subscription.objects.get_or_create(
                    user_membership=user_membership)
                sub.stripe_subscription_id = user_stripe_subscription[0].id
                sub.active = True
                sub.save()
        else:
            # If stripe subscription not active, move to free local subscription and make subscription inactive
            user_membership.membership = Membership.objects.get(membership_type='Free')
            user_membership.save()

            sub, created = Subscription.objects.get_or_create(
                user_membership=user_membership)
            sub.stripe_subscription_id = user_stripe_subscription[0].id
            sub.active = False
            sub.save()
    else:
        # If no stripe subscription, move to free local subscription
        user_membership.membership = Membership.objects.get(membership_type='Free')
        user_membership.save()


def get_stripe_subscriptions(customer_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        subscriptions = stripe.Subscription.list(customer=customer_id)
        return subscriptions.data
    except stripe.error.StripeError as e:
        print(f"Error: {e}")
        return []


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


@login_required(login_url='/authentication/login')
def MembershipSelectView(request):
    if request.method == 'GET':
        user_membership = get_user_membership(request)
        current_membership = get_user_membership(request)
        user_stripe_subscription = get_stripe_subscriptions(user_membership.stripe_customer_id)

        if user_stripe_subscription:
            return redirect(reverse("customer_portal"))

        context = {
            "current_membership": str(current_membership.membership.membership_type),
            'user_membership': user_membership,
            'customer_id': stripe.Customer.retrieve(user_membership.stripe_customer_id),
            'user': request.user,
            'object_list': Membership.objects.all()

        }
        return render(request, 'payment/membership_list.html', context)

    if request.method == 'POST':
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.POST.get('membership_type')

        selected_membership = Membership.objects.get(
            membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                messages.info(request, """You already have this membership. Your
                              next payment is due {}""".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('payment'))


@login_required(login_url='/authentication/login')
def CustomerPortalView(request):
    user_membership = get_user_membership(request)
    customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
    current_membership = get_user_membership(request)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.billing_portal.Configuration.create(
        business_profile={
            "headline": "Cactus Practice partners with Stripe for simplified billing.",
        },
        features={"invoice_history": {"enabled": True}},
    )
    session = stripe.billing_portal.Session.create(
        customer=user_membership.stripe_customer_id,
        return_url=request.build_absolute_uri(reverse("choose-create-speed")),
    )
    return redirect(session.url)


@login_required(login_url='/authentication/login')
def CheckoutView(request):
    user_membership = get_user_membership(request)
    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("payment-plans"))
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': selected_membership.stripe_plan_id,
                    'quantity': 1,
                },
            ],
            customer=user_membership.stripe_customer_id,
            mode='subscription',
            success_url=request.build_absolute_uri(reverse("payment-success")),
            cancel_url=request.build_absolute_uri(reverse("payment-plans")),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return "Server error", 500


"""
Will go here only when in FREE plan and Successfully purchased a subscription
"""
@login_required(login_url='/authentication/login')
def payment_success_view(request):

    # Update user membership from FREE to the selected one
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    # Create a subscription for the user
    user_stripe_subscription = get_stripe_subscriptions(user_membership.stripe_customer_id)
    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = user_stripe_subscription[0].id
    sub.active = True
    sub.save()

    context = {
        "user_membership": str(user_membership.membership.membership_name),
    }
    return render(request, "payment/success.html", context)
