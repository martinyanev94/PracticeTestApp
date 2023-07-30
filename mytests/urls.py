from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.my_tests, name="my-tests"),
    path('edit-test/<int:id>', views.edit_pt, name="edit-test"),
    path('delete-test/<int:id>', views.delete_pt, name="delete-test"),
    path('search-test', csrf_exempt(views.search_tests), name="search-test")

]