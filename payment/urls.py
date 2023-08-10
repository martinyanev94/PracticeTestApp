from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_plans, name='payment-plans'),

]