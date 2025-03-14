from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('login/', views.login_view, name='login'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/new/', views.create_report, name='create_report'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]