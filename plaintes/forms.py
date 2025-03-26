from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Report, User, Comment

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'placeholder': "Nom d'utilisateur"})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmer le mot de passe'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise ValidationError("Le numéro de téléphone ne doit contenir que des chiffres.")
        return phone

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['description', 'problem_type', 'location', 'media']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez le problème en détail'
            }),
            'problem_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'adresse ou la localisation'
            }),
            'media': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            # Vérifier la taille du fichier (max 5MB)
            if media.size > 5 * 1024 * 1024:
                raise ValidationError("Le fichier est trop volumineux. La taille maximale est de 5MB.")
            
            # Vérifier le type de fichier
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4']
            if media.content_type not in allowed_types:
                raise ValidationError("Type de fichier non autorisé. Formats acceptés : JPEG, PNG, GIF, MP4")
        return media

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre commentaire...'
            })
        }

class ReportFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher...'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + list(Report.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    problem_type = forms.ChoiceField(
        choices=[('', 'Tous les types')] + list(Report.PROBLEM_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
