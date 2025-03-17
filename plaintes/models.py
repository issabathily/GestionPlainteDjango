from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    ROLES = (
        ('citizen', 'Citoyen'),
        ('admin', 'Administrateur'),
        ('moderator', 'Modérateur'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='citizen')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Report(models.Model):
    PROBLEM_TYPES = (
        ('waste', 'Déchets'),
        ('road', 'Routes endommagées'),
        ('water', 'Coupures d\'eau'),
        ('electricity', 'Problèmes électriques'),
        ('other', 'Autres'),
    )
    STATUS_CHOICES = (
        ('received', 'Reçu'),
        ('in_progress', 'En cours'),
        ('rejected', 'Rejeté'),
        ('resolved', 'Résolu'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES, default='other')
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"Plainte {self.id} - {self.status}"

class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire par {self.user}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
