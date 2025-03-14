from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Report, Notification
from .forms import ReportForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'plaintes/login.html', {'form': form})

@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'plaintes/report_list.html', {'reports': reports})

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'plaintes/report_detail.html', {'report': report})

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            Notification.objects.create(user=request.user, report=report, message=f"Plainte {report.id} créée.")
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportForm()
    return render(request, 'plaintes/create_report.html', {'form': form})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'plaintes/notification_list.html', {'notifications': notifications})

@login_required
def dashboard(request):
    reports = Report.objects.filter(user=request.user) if request.user.role == 'citizen' else Report.objects.all()
    stats = {
        'total': reports.count(),
        'resolved': reports.filter(status='resolved').count(),
        'in_progress': reports.filter(status='in_progress').count(),
    }
    return render(request, 'plaintes/dashboard.html', {'stats': stats})