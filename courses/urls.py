from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('<int:course_id>/', views.course_detail, name='detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll'),
    path('<int:course_id>/module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
] 