from django.contrib import admin
from .models import User, Comment, Notification, Report  # Note que tu n'as pas besoin de "AbstractUser" ici

# Enregistrer le modèle Comment
admin.site.register(Comment)
admin.site.register(Notification)

# Configuration pour le modèle User
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'email', 'is_staff', 'is_active']  # Afficher certains champs
    search_fields = ['username', 'email']  # Permettre de chercher par ces champs

# Configuration pour le modèle Report
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'status', 'user', 'created_at']  # Afficher certains champs
    list_filter = ['status', 'created_at']  # Ajouter des filtres par statut et date

# Enregistrer les modèles avec leurs configurations d'administration personnalisées
admin.site.register(User, UserAdmin)
admin.site.register(Report, ReportAdmin)
