from django.urls import path
from . import views
from .views import MembershipSelectView, PaymentView, updateTransactionRecords, cancelSubscription

urlpatterns = [
    path('', MembershipSelectView.as_view(), name='payment-plans'),
    path('payment/', PaymentView, name='payment'),
    path('update-transactions/<subscription_id>/',
         updateTransactionRecords, name='update-transactions'),
    path('cancel/', cancelSubscription, name='cancel')

]