from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificate_list, name='list'),
    path('<int:certificate_id>/', views.certificate_detail, name='detail'),
    path('<int:certificate_id>/download/', views.download_certificate, name='download'),
] 