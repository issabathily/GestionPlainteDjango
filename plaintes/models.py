from django.contrib.auth.models import AbstractUser
from django.db import models


# Définition d'un modèle User personnalisé en héritant d'AbstractUser
class User(AbstractUser):
    # Définition des rôles disponibles pour les utilisateurs
    ROLES = (
        ('citizen', 'Citoyen'),  # Rôle de citoyen
        ('admin', 'Administrateur'),  # Rôle d'administrateur
        ('moderator', 'Modérateur'),  # Rôle de modérateur
    )

    # Champ pour stocker le rôle de l'utilisateur
    role = models.CharField(max_length=20, choices=ROLES, default='citizen')

    # Champ pour stocker le numéro de téléphone de l'utilisateur, facultatif
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Méthode pour retourner le nom d'utilisateur
    def __str__(self):
        return self.username


# Modèle pour gérer les rapports d'incidents
class Report(models.Model):
    # Types de problèmes pouvant être signalés
    PROBLEM_TYPES = (
        ('waste', 'Déchets'),  # Problèmes liés aux déchets
        ('road', 'Routes endommagées'),  # Problèmes de routes
        ('water', 'Coupures d\'eau'),  # Problèmes d'approvisionnement en eau
        ('electricity', 'Problèmes électriques'),  # Problèmes d'électricité
        ('other', 'Autres'),  # Autres types de problèmes
    )

    # Statuts possibles d'un rapport
    STATUS_CHOICES = (
        ('received', 'Reçu'),  # Rapport reçu
        ('in_progress', 'En cours'),  # Rapport en cours de traitement
        ('rejected', 'Rejeté'),  # Rapport rejeté
        ('resolved', 'Résolu'),  # Rapport résolu
    )

    # Lien vers l'utilisateur qui a créé le rapport
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Champ pour décrire le problème
    description = models.TextField()

    # Champ pour indiquer le type de problème
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES, default='other')

    # Champ pour spécifier l'emplacement du problème
    location = models.CharField(max_length=255)

    # Champ pour le statut du rapport
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')

    # Date et heure de création du rapport
    created_at = models.DateTimeField(auto_now_add=True)

    # Date et heure de la dernière mise à jour du rapport
    updated_at = models.DateTimeField(auto_now=True)

    # Champ pour les fichiers attachés au rapport (images, documents, etc.)
    media = models.FileField(upload_to='reports/', blank=True, null=True)

    # Méthode pour retourner une représentation lisible du rapport
    def __str__(self):
        return f"Plainte {self.id} - {self.status}"


# Modèle pour les commentaires sur les rapports
class Comment(models.Model):
    # Lien vers le rapport auquel le commentaire est associé
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')

    # Lien vers l'utilisateur qui a fait le commentaire
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Contenu du commentaire
    content = models.TextField()

    # Date et heure de création du commentaire
    created_at = models.DateTimeField(auto_now_add=True)

    # Méthode pour retourner une représentation lisible du commentaire
    def __str__(self):
        return f"Commentaire par {self.user}"


# Modèle pour les notifications liées aux rapports
class Notification(models.Model):
    # Lien vers l'utilisateur qui reçoit la notification
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Lien vers le rapport associé à la notification (peut être null)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)

    # Message de la notification
    message = models.CharField(max_length=255)

    # Indicateur de lecture de la notification
    is_read = models.BooleanField(default=False)

    # Date et heure de création de la notification
    created_at = models.DateTimeField(auto_now_add=True)

    # Méthode pour retourner une représentation lisible de la notification
    def __str__(self):
        return self.message
