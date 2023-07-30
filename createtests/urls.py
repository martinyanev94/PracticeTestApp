from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_create_speed, name='choose-create-speed'),
    path('quick-test', views.quick_test, name='quick-test'),
    path('advanced-test', views.advanced_test, name='advanced-test'),

]
