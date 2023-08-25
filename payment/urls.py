from django.urls import path
from . import views
from .views import MembershipSelectView, PaymentView, updateTransactionRecords, profile_view, cancelSubscription

urlpatterns = [
    path('', views.payment_plans, name='payment-plans'),
    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/',
         updateTransactionRecords, name='update-transactions'),
    path('profile/', profile_view, name='profile'),
    path('cancel/', cancelSubscription, name='cancel')

]