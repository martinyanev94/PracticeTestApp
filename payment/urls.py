from django.urls import path
from .views import MembershipSelectView, CustomerPortalView, \
    CheckoutView, payment_success_view

urlpatterns = [
    path('', MembershipSelectView, name='payment-plans'),
    path('payment/', CheckoutView, name='payment'),
    path('customer_portal/', CustomerPortalView, name='customer_portal'),
    path('success/', payment_success_view, name='payment-success'),

]