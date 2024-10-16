from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings

from cabinet.models import Article
from compte.models import User
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
#

# from dotenv import load_dotenv
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.def login_page(request):
##################


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ArticleForm, LoginForm, SignupForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model  # Pour utiliser le modèle d'utilisateur personnalisé

#########################

User = get_user_model()

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                print("email:",email)
                # On cherche d'abord un utilisateur ayant cet email
                user = User.objects.get(email=email)
                print("userrr",user)
                # Ensuite, on vérifie que le mot de passe est correct
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('compte:dashboard')  # Redirige vers le tableau de bord après connexion
                else:
                    form.add_error(None, 'Identifiants invalides.')
            except User.DoesNotExist:
                form.add_error(None, "Aucun utilisateur n'est enregistré avec cet email.")
    else:
        form = LoginForm()

    return render(request, 'compte/login.html', {'form': form})
######################
def signup_page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print("email:",email,"username:",username)
            # Créer l'utilisateur avec un mot de passe haché
            # Création manuelle de l'utilisateur avec hachage du mot de passe
            user = User(username=username, email=email)
            user.set_password(password)  # Hacher manuellement le mot de passe
            user.save()
            
            return redirect('compte:login')
    else:
        form = SignupForm()

    return render(request, 'compte/signup.html', {'form': form})

##################
def logout_user(request):
    logout(request)
    
    return redirect('cabinet:homepage')

#profile user
##################
@login_required
def profile(request):
    return render(request,'compte/profile_user.html')

##################
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('nouveau_mot_de_passe'):
                update_session_auth_hash(request, user)  # Met à jour la session pour éviter la déconnexion
            # messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('pro_commerce:homepage')
    else:
        form = forms.UserProfileForm(instance=user)
    
    return render(request, 'compte/profile_user.html', {'form': form})

##################
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('pro_commerce:homepage')  # Redirigez vers une page d'accueil ou de connexion après suppression
    return redirect('compte:profile')

##################
def password_reset_complete(request):
    return render(request, 'compte/password_reset_complete.html')
#################
def dashboard_admin(request):
    articles=Article.objects.all()
    
    context={
        'article':articles
    }
    return render(request,'compte/admin/admin.html',context)

# #
# def profile(request):
#     return render(request,'compte/profile.html')
@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('nouveau_mot_de_passe'):
                update_session_auth_hash(request, user)  # Met à jour la session pour éviter la déconnexion
            # messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('pro_commerce:homepage')
    else:
        form = forms.UserProfileForm(instance=user)
    
    return render(request, 'compte/profile_user.html', {'form': form})
#
@login_required
def article_delete(request, slug=None):
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, " L\'article a été supprimé avec succès.")

        return redirect('compte:dashboard')
        
    # Optionally, you can render a confirmation page here if not using a modal
        # return render(request,'compte/admin/admin.html')

    return redirect('compte:dashboard')
#
@login_required
def add_article(request):
    if request.method == 'POST':
        # Initialize the form with POST data and files
        form = ArticleForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the main product instance without committing yet
            article = form.save(commit=False)
            article.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            article.save()  # Save product first

          
            
            messages.success(request, " L\'article a été enregistré avec succès.")
            return redirect('compte:dashboard')
        else:
            messages.error(request, "Erreur lors de l\'enregistrement de l\'article Veuillez vérifier les informations.")
    else:
        form = ArticleForm()

    return render(request, 'compte/admin/article/add_article.html', {'form': form})
##


@login_required
def article_update(request, slug=None):
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            # Sauvegarde du produit, y compris la photo si un nouveau fichier est téléchargé
            article = form.save(commit=False)
            article.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            article.save()  # Save product first

            messages.success(request, " L\'article a été mis à jour avec succès.")
            return redirect('compte:dashboard')
        else:
            # Ajout de messages d'erreur spécifiques pour le formulaire
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations saisies.')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'compte/admin/article/article_update.html', {'form': form})