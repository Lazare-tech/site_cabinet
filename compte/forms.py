from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from cabinet.models import Article, Articlecategorie, Services,categories_services  # Pour utiliser le modèle d'utilisateur personnalisé
from django_ckeditor_5.widgets import CKEditor5Widget

User = get_user_model()  # Récupère le modèle d'utilisateur personnalisé

class LoginForm(forms.Form):
    # Utilisation de l'email pour la connexion
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=63,
        label="Email",
        error_messages={
            'required': _('Le mail est requis.'),
            'invalid': _('Veuillez entrer une adresse email valide.')
        }
    )

    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Mot de passe',
        error_messages={
            'required': _('Le mot de passe est requis.')
        }
    )

class SignupForm(forms.ModelForm):  # Utilisation de ModelForm pour se baser sur le modèle User
    username = forms.CharField(
        max_length=63,
        label=_('Nom d’utilisateur'),
        error_messages={
            'required': _('Le nom d’utilisateur est requis.'),
            'max_length': _('Le nom d’utilisateur ne peut pas dépasser 63 caractères.')
        },
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label=_('Email'),
        error_messages={
            'required': _('Le mail est requis.'),
            'invalid': _('Veuillez entrer une adresse email valide.')
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=_('Mot de passe'),
        min_length=6,
        error_messages={
            'required': _('Le mot de passe est requis.'),
            'min_length': _('Le mot de passe doit contenir au moins 6 caractères.')
        }
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=_('Confirmer le mot de passe'),
        error_messages={
            'required': _('La confirmation du mot de passe est requise.')
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Les mots de passe ne correspondent pas.'))

    class Meta:
        model = User  # Utilisation du modèle User personnalisé
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }
#####
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['photo', 'titre', 'article', 'contenu']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': CKEditor5Widget(config_name='extends'),
                        

            'article': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nom(self):
        titre = self.cleaned_data.get('titre')
        if len(titre) > 40:
            raise forms.ValidationError("Le titre de l'article ne peut pas dépasser 40 caractères.")
        return titre
##
class UserProfileForm(forms.ModelForm):
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        label="Nouveau mot de passe",
        required=False
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmer le mot de passe",
        required=False
    )
    
    
    class Meta:
        model = User
        fields = ['username','email']
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            # 'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'confirmer_mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),



            
        }
        
class ArticleCategorieForm(forms.ModelForm):
    # Define the field for secondary images correctly

    class Meta:
        model = Articlecategorie
        fields = ['nom_article']
        widgets = {
            'nom_article': forms.TextInput(attrs={'class': 'form-control'}),
           

          
        }
    def clean_nom(self):
        nom_article = self.cleaned_data.get('nom_article')
        if len(nom_article) > 40:
            raise forms.ValidationError("Le nom ne peut pas dépasser 40 caractères.")
        return nom_article
    ########################
    #CATEGORIES SERVICES
class ServiceCategorieForm(forms.ModelForm):
    # Define the field for secondary images correctly

    class Meta:
        model = categories_services
        fields = ['categorie_service']
        widgets = {
            'categorie_service': forms.TextInput(attrs={'class': 'form-control'}),
           

          
        }
    def clean_nom(self):
        categorie_service = self.cleaned_data.get('categorie_service')
        if len(categorie_service) > 40:
            raise forms.ValidationError("Le nom ne peut pas dépasser 40 caractères.")
        return categorie_service
    ##############################
    #SERVICE
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['image_service', 'nom_service']
        widgets = {
            'image_service': forms.FileInput(attrs={'class': 'form-control'}),
                        

            'nom_service': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nom(self):
        nom_service = self.cleaned_data.get('nom_service')
        if len(nom_service) > 40:
            raise forms.ValidationError("Le nom du service ne peut pas dépasser 40 caractères.")
        return nom_service
##