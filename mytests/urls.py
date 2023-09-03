from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.my_tests, name="my-tests"),
    path('edit-test/<int:id>', views.edit_pt, name="edit-test"),
    path('home-view/<int:id>', views.home_view, name="home-view"),
    path('home-view/', views.home_view, name="home-view-clean"),
    path('delete-test/<int:id>', views.delete_pt, name="delete-test"),
    path('search-test', csrf_exempt(views.search_tests), name="search-test"),
    path('download-student-view/<int:id>/', views.download_student_view, name='download-student-view'),
    path('download-teacher-view/<int:id>/', views.download_teacher_view, name='download-teacher-view'),
    path('download-teacher-view-pdf/<int:id>/', views.download_teacher_view_pdf, name='download-teacher-view-pdf'),
    path('download-student-view-pdf/<int:id>/', views.download_student_view_pdf, name='download-student-view-pdf'),
    path('download-teacher-view-txt/<int:id>/', views.download_teacher_view_txt, name='download-teacher-view-txt'),
    path('download-student-view-txt/<int:id>/', views.download_student_view_txt, name='download-student-view-txt'),

]