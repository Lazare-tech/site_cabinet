from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from cabinet.models import Article, Articlecategorie, ContactMessage, Services, contact_information,expertise  # Pour utiliser le modèle d'utilisateur personnalisé
from django_ckeditor_5.widgets import CKEditor5Widget
import phonenumbers
from phonenumbers import NumberParseException
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
        model = expertise
        fields = ['expertise']
        widgets = {
            'expertise': forms.TextInput(attrs={'class': 'form-control'}),
           

          
        }
    def clean_nom(self):
        expertise = self.cleaned_data.get('expertise')
        if len(expertise) > 40:
            raise forms.ValidationError("Le nom ne peut pas dépasser 40 caractères.")
        return expertise
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
# class ContactMessageForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['nom', 'email', 'numero_telephone', 'objet', 'contenu']
#         widgets = {
#             'nom': forms.TextInput(attrs={
#                 'class': 'form-control border-input-part',
#                 'id': 'nom',
#                 'name': 'nom',
#                 'placeholder': 'Entrez votre nom complet',
#                 'required': 'required'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'id': 'email',
#                 'name': 'email',
#                 'placeholder': 'Entrez votre email',
#                 'required': 'required'
#             }),
#             'numero_telephone': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'numero_telephone',
#                 'name': 'numero_telephone',
#                 'placeholder': 'Entrez votre numéro de téléphone'
#             }),
#             'objet': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'objet',
#                 'name': 'objet',
#                 'placeholder': "Entrez l'objet",
#                 'required': 'required'
#             }),
#             'contenu': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'id': 'contenu',
#                 'name': 'contenu',
#                 'rows': '3',
#                 'placeholder': 'Votre message',
#                 'required': 'required'
#             }),
#         }
#         labels = {
#             'nom': 'Nom complet',
#             'email': 'Email',
#             'numero_telephone': 'Numéro de téléphone',
#             'objet': 'Objet',
#             'contenu': 'Message',
#   
from django.core.exceptions import ValidationError

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['nom', 'email', 'numero_telephone', 'objet', 'contenu']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'}),
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre numéro de téléphone',
                'id': 'telephone',  # requis par intl-tel-input
                'type': 'tel'
            }),
            'objet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Entrez l'objet du message"}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': "Votre message"}),
        }

    def clean_contenu(self):
        contenu = self.cleaned_data.get('contenu')
        if len(contenu) > 255:
            raise forms.ValidationError("Le message ne peut pas dépasser 255 caractères.")
        return contenu

    def clean_numero_telephone(self):
        numero = self.cleaned_data.get('numero_telephone')

        try:
            # Analyse sans pays par défaut, car intl-tel-input envoie le numéro international complet
            phone = phonenumbers.parse(numero, None)

            # Vérifie si le numéro est valide
            if not phonenumbers.is_valid_number(phone):
                raise ValidationError("Numéro de téléphone invalide.")

            # Formate en format E.164 : ex. +22670000000
            numero_formatte = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            return numero_formatte

        except NumberParseException:
            raise ValidationError("Format de numéro de téléphone incorrect.")

######
class enterprise_contactForm(forms.ModelForm):
      class Meta:
        model = contact_information
        fields = ['nom_entreprise', 'email', 'numero_telephone', 'localisation']
        widgets = {
            'nom_entreprise': forms.TextInput(attrs={'class': 'form-control border', 'placeholder': 'Entrez le nom de l\'entreprise '}),

            'localisation': forms.TextInput(attrs={'class': 'form-control border', 'placeholder': 'Entrez votre localisation'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border', 'placeholder': 'Entrez votre email'}),
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control border',
                'placeholder': 'Entrez votre numéro de téléphone',
                'id': 'telephone',  # requis par intl-tel-input
                'type': 'tel'
            }),
                }
    