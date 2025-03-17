from django.shortcuts import render, redirect, get_object_or_404  # Importation des fonctions pour gérer les vues
from django.contrib.auth import login, logout, authenticate  # Importation des fonctions d'authentification
from django.contrib.auth.decorators import login_required  # Décorateur pour restreindre l'accès
from django.db.models import Count  # Pour les requêtes de comptage
from django.core.paginator import Paginator  # Pour la pagination
from .models import User, Report, Comment, Notification  # Importation des modèles
from .forms import SignUpForm, LoginForm, ReportForm, CommentForm  # Importation des formulaires
from django.http import JsonResponse  # Pour les réponses JSON
import json  # Pour le traitement JSON


def home(request):
    # Redirection en fonction du statut de l'utilisateur
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('tableau_de_bord_admin')  # Redirige vers le tableau de bord admin
        else:
            return redirect('tableau_de_bord_citoyen')  # Redirige vers le tableau de bord citoyen
    return render(request, 'plaintes/home.html')  # Affiche la page d'accueil


def signup_view(request):
    # Gestion de l'inscription des utilisateurs
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Création d'un formulaire avec les données POST
        if form.is_valid():  # Validation du formulaire
            user = form.save()  # Enregistrement de l'utilisateur
            login(request, user)  # Connexion de l'utilisateur
            return redirect('tableau_de_bord_admin' if user.is_staff else 'tableau_de_bord_citoyen')
    else:
        form = SignUpForm()  # Affiche un formulaire vide pour l'inscription
    return render(request, 'plaintes/signup.html', {'form': form})  # Affiche la page d'inscription


def login_view(request):
    # Gestion de la connexion des utilisateurs
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Création d'un formulaire avec les données POST
        if form.is_valid():  # Validation du formulaire
            username = form.cleaned_data.get('username')  # Récupération du nom d'utilisateur
            password = form.cleaned_data.get('password')  # Récupération du mot de passe
            user = authenticate(username=username, password=password)  # Authentification de l'utilisateur
            if user is not None:  # Vérification de l'utilisateur
                login(request, user)  # Connexion de l'utilisateur
                return redirect('tableau_de_bord_admin' if user.is_staff else 'tableau_de_bord_citoyen')
    else:
        form = LoginForm()  # Affiche un formulaire vide pour la connexion
    return render(request, 'plaintes/login.html', {'form': form})  # Affiche la page de connexion


def logout_view(request):
    logout(request)  # Déconnexion de l'utilisateur
    return redirect('home')  # Redirection vers la page d'accueil


@login_required
def tableau_de_bord_admin(request):
    # Vue pour le tableau de bord administrateur
    if request.user.role != 'admin':
        return redirect('home')  # Redirection si l'utilisateur n'est pas admin

    # Statistiques globales
    total_rapports = Report.objects.count()  # Nombre total de rapports
    rapports_resolus = Report.objects.filter(status='resolved').count()  # Nombre de rapports résolus
    rapports_en_attente = Report.objects.exclude(status='resolved').count()  # Nombre de rapports en attente
    total_utilisateurs = User.objects.count()  # Nombre total d'utilisateurs

    # Récupérer les rapports récents
    rapports_recents = Report.objects.order_by('-created_at')[:5]  # 5 rapports les plus récents

    context = {
        'total_rapports': total_rapports,
        'rapports_resolus': rapports_resolus,
        'rapports_en_attente': rapports_en_attente,
        'total_utilisateurs': total_utilisateurs,
        'rapports_recents': rapports_recents,
    }

    return render(request, 'plaintes/tableau_de_bord_admin.html', context)  # Affiche le tableau de bord admin


@login_required
def tableau_de_bord_citoyen(request):
    # Vue pour le tableau de bord citoyen
    rapports_utilisateur = Report.objects.filter(user=request.user)  # Récupérer les rapports de l'utilisateur connecté

    # Statistiques des rapports de l'utilisateur
    total_rapports = rapports_utilisateur.count()  # Nombre total de rapports de l'utilisateur
    rapports_resolus = rapports_utilisateur.filter(status='resolved').count()  # Nombre de rapports résolus
    rapports_en_attente = rapports_utilisateur.exclude(status='resolved').count()  # Nombre de rapports en attente

    # Récupérer les rapports récents de l'utilisateur
    rapports_recents = rapports_utilisateur.order_by('-created_at')[:5]  # 5 rapports les plus récents

    context = {
        'total_rapports': total_rapports,
        'rapports_resolus': rapports_resolus,
        'rapports_en_attente': rapports_en_attente,
        'rapports_recents': rapports_recents,
    }

    return render(request, 'plaintes/tableau_de_bord_citoyen.html', context)  # Affiche le tableau de bord citoyen


@login_required
def report_list(request):
    # Vue pour lister les rapports
    reports = Report.objects.all()  # Récupérer tous les rapports
    if request.user.role != 'admin':
        reports = reports.filter(user=request.user)  # Filtrer les rapports pour l'utilisateur connecté si non admin

    # Filtrage
    status = request.GET.get('status')  # Récupérer le paramètre de statut
    problem_type = request.GET.get('type')  # Récupérer le paramètre de type de problème
    search = request.GET.get('search')  # Récupérer le paramètre de recherche
    sort = request.GET.get('sort', '-created_at')  # Récupérer le paramètre de tri (par défaut par date de création)

    if status:
        reports = reports.filter(status=status)  # Filtrer par statut
    if problem_type:
        reports = reports.filter(problem_type=problem_type)  # Filtrer par type de problème
    if search:
        reports = reports.filter(description__icontains=search)  # Filtrer par recherche dans la description

    # Tri
    reports = reports.order_by(sort)  # Tri des rapports

    # Pagination
    paginator = Paginator(reports, 12)  # Pagination avec 12 rapports par page
    page = request.GET.get('page')  # Récupérer le numéro de page
    reports = paginator.get_page(page)  # Récupérer la page des rapports

    context = {
        'reports': reports,
        'current_status': status,
        'current_type': problem_type,
        'current_search': search,
        'current_sort': sort
    }
    return render(request, 'plaintes/report_list.html', context)  # Affiche la liste des rapports


@login_required
def create_report(request):
    # Vue pour créer un rapport
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)  # Création d'un formulaire avec les données POST et fichiers
        if form.is_valid():  # Validation du formulaire
            report = form.save(commit=False)  # Créer un rapport sans l'enregistrer
            report.user = request.user  # Assignation de l'utilisateur connecté au rapport
            report.save()  # Enregistrement du rapport
            return redirect('report_detail', report_id=report.id)  # Redirection vers les détails du rapport
    else:
        form = ReportForm()  # Affiche un formulaire vide pour la création de rapport
    return render(request, 'plaintes/create_report.html', {'form': form})  # Affiche la page de création de rapport


@login_required
def report_detail(request, report_id):
    # Vue pour afficher les détails d'un rapport
    report = get_object_or_404(Report, id=report_id)  # Récupérer le rapport ou 404 si non trouvé
    if request.user.role != 'admin' and report.user != request.user:
        return redirect('dashboard')  # Redirection si l'utilisateur n'est pas autorisé à voir le rapport

    if request.method == 'POST':
        form = CommentForm(request.POST)  # Création d'un formulaire de commentaire avec les données POST
        if form.is_valid():  # Validation du formulaire
            comment = form.save(commit=False)  # Créer un commentaire sans l'enregistrer
            comment.report = report  # Assigner le rapport au commentaire
            comment.user = request.user  # Assigner l'utilisateur au commentaire
            comment.save()  # Enregistrement du commentaire

            # Créer une notification pour le propriétaire du rapport
            if request.user != report.user:
                Notification.objects.create(
                    user=report.user,
                    report=report,
                    message=f"Nouveau commentaire sur votre rapport de {request.user.username}"
                )

            return redirect('report_detail', report_id=report.id)  # Redirection vers les détails du rapport
    else:
        form = CommentForm()  # Affiche un formulaire vide pour ajouter un commentaire

    context = {
        'report': report,
        'comments': report.comments.all().order_by('-created_at'),  # Récupérer tous les commentaires triés par date
        'form': form
    }
    return render(request, 'plaintes/report_detail.html', context)  # Affiche les détails du rapport


@login_required
def delete_report(request, report_id):
    # Vue pour supprimer un rapport
    report = get_object_or_404(Report, id=report_id)  # Récupérer le rapport ou 404 si non trouvé
    if request.user != report.user and request.user.role != 'admin':
        return redirect('dashboard')  # Redirection si l'utilisateur n'est pas autorisé à supprimer le rapport

    if request.method == 'POST':
        report.delete()  # Suppression du rapport
        return redirect('report_list')  # Redirection vers la liste des rapports

    return render(request, 'plaintes/delete_report_confirm.html',
                  {'report': report})  # Affiche la confirmation de suppression


@login_required
def update_report_status(request, report_id):
    # Vue pour mettre à jour le statut d'un rapport
    if request.method != 'POST' or request.user.role != 'admin':
        from django.http import HttpResponseForbidden  # Importation pour le refus d'accès
        return HttpResponseForbidden()  # Renvoie une réponse 403 Forbidden

    try:
        data = json.loads(request.body)  # Chargement des données JSON du corps de la requête
        new_status = data.get('status')  # Récupérer le nouveau statut

        if not new_status or new_status not in dict(Report.STATUS_CHOICES):
            return JsonResponse({'error': 'Statut invalide'}, status=400)  # Erreur si statut invalide

        report = get_object_or_404(Report, id=report_id)  # Récupérer le rapport ou 404 si non trouvé
        old_status = report.status  # Récupérer l'ancien statut
        report.status = new_status  # Mettre à jour le statut
        report.save()  # Enregistrement du rapport

        # Créer une notification pour l'utilisateur
        if old_status != new_status:
            Notification.objects.create(
                user=report.user,
                report=report,
                message=f"Le statut de votre rapport a été mis à jour : {dict(Report.STATUS_CHOICES)[new_status]}"
            )

        return JsonResponse({
            'status': 'success',
            'new_status': new_status,
            'status_display': dict(Report.STATUS_CHOICES)[new_status]
        })  # Retourne une réponse JSON de succès

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)  # Erreur de décodage JSON
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)  # Erreur générale


@login_required
def notification_list(request):
    # Vue pour lister les notifications de l'utilisateur
    notifications = Notification.objects.filter(user=request.user).order_by(
        '-created_at')  # Récupérer les notifications triées par date
    return render(request, 'plaintes/notification_list.html',
                  {'notifications': notifications})  # Affiche la liste des notifications


@login_required
def mark_notification_read(request, notification_id):
    # Vue pour marquer une notification comme lue
    notification = get_object_or_404(Notification, id=notification_id,
                                     user=request.user)  # Récupérer la notification ou 404 si non trouvée
    notification.is_read = True  # Marquer la notification comme lue
    notification.save()  # Enregistrement de la notification
    return redirect('notification_list')  # Redirection vers la liste des notifications
