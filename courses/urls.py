from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/complete/', views.complete_course, name='complete_course'),
    path('<int:course_id>/module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/update/', views.course_update, name='course_update'),
    path('<int:course_id>/delete/', views.course_delete, name='course_delete'),
]