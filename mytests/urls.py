from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.my_tests, name="my-tests"),
    path('edit-test/<int:id>', views.edit_pt, name="edit-test"),
    path('home-view/<int:id>', views.home_view, name="home-view"),
    path('delete-test/<int:id>', views.delete_pt, name="delete-test"),
    path('search-test', csrf_exempt(views.search_tests), name="search-test"),
    path('download-student-view/<int:id>/', views.download_student_view, name='download-student-view'),
    path('download-teacher-view/<int:id>/', views.download_teacher_view, name='download-teacher-view'),

]