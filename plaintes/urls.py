from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('tableau-de-bord-admin/', views.tableau_de_bord_admin, name='tableau_de_bord_admin'),
    path('tableau-de-bord-citoyen/', views.tableau_de_bord_citoyen, name='tableau_de_bord_citoyen'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Gestion des rapports
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<int:report_id>/delete/', views.delete_report, name='delete_report'),
    path('reports/<int:report_id>/update-status/', views.update_report_status, name='update_report_status'),
    
    # Notifications
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]
