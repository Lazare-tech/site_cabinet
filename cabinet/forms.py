from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from cabinet.models import  News_letter  # Pour utiliser le modèle d'utilisateur personnalisé
from django_ckeditor_5.widgets import CKEditor5Widget
import phonenumbers
from phonenumbers import NumberParseException
class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = News_letter
        fields = ['email',]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'}),
        }
        labels = {
            'email': 'Adresse Email',
        }
