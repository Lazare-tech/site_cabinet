from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings
from django.views import View

from cabinet.models import Article, Articlecategorie, Services, categories_services
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
from .forms import ArticleCategorieForm, ArticleForm, LoginForm, ServiceCategorieForm, ServiceForm, SignupForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model  # Pour utiliser le modèle d'utilisateur personnalisé
from cabinet import context_processors
#########################
from .mixins import GlobalData
##
    
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
    if request.user.is_authenticated:
        
        articles=Article.objects.all().order_by('-date_publie')
    
        context={
        'article':articles
        }
    else:
        return redirect('compte:login')
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
            return redirect('compte:dashboard')
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
######################ARTICLE CATEGORIE

def article_categorie(request):
    categorie_article=Articlecategorie.objects.all()
    nombre_categorie_article=categorie_article.count()
    #
    article=Article.objects.all()
    nombre_article=article.count()
    

    context={
        'article':article,
        'categorie_article':categorie_article,
        'nombre_article':nombre_article,
        'nombre_categorie_article':nombre_categorie_article
    }
    return render(request,'compte/admin/article/article_categorie.html',context)
#


    return context
@login_required
def add_categorie_article(request):
    if request.method == 'POST':
        # Initialize the form with POST data and files
        form = ArticleCategorieForm(request.POST)
        
        if form.is_valid():
            # Save the main product instance without committing yet
            categorie_article = form.save(commit=False)
            categorie_article.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            categorie_article.save()  # Save product first

          
            
            messages.success(request, " L\'article a été enregistré avec succès.")
            return redirect('compte:article')
        else:
            messages.error(request, "Erreur lors de l\'enregistrement de l\'article Veuillez vérifier les informations.")
    else:
        form = ArticleCategorieForm()

    return render(request, 'compte/admin/article/add_categorie.html', {'form': form})    
##

@login_required
def categorie_article_delete(request, slug=None):
    article = get_object_or_404(Articlecategorie, slug=slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, " La categorie a été supprimé avec succès.")

        return redirect('compte:article')
        
    # Optionally, you can render a confirmation page here if not using a modal
        # return render(request,'compte/admin/admin.html')

    return redirect('compte:article')
#

@login_required
def categorie_article_update(request, slug=None):
    categorie_article = get_object_or_404(Articlecategorie, slug=slug)
    print("okk")
    if request.method == 'POST':
        form = ArticleCategorieForm(request.POST, request.FILES, instance=categorie_article)
        if form.is_valid():
            # Sauvegarde du produit, y compris la photo si un nouveau fichier est téléchargé
            categorie_article = form.save(commit=False)
            categorie_article.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            categorie_article.save()  # Save product first

            messages.success(request, " L\'article a été mis à jour avec succès.")
            return redirect('compte:article')
        else:
            # Ajout de messages d'erreur spécifiques pour le formulaire
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations saisies.')
    else:
        form = ArticleCategorieForm(instance=categorie_article)

    return render(request, 'compte/admin/article/update_categorie_article.html', {'form': form})
################################################################
#CATEGORIES SERVICES
def service_categorie(request):
    categorie_ser=categories_services.objects.all()
    # #
    article=Article.objects.all()
    nombre_article=article.count()

    context={
        # 'article':article,
        'categorie_service':categorie_ser,
        'nombre_article':nombre_article,
    }
    return render(request,'compte/admin/service/service_categorie.html',context)
#

@login_required
def add_categorie_service(request):
    if request.method == 'POST':
        # Initialize the form with POST data and files
        form =  ServiceCategorieForm(request.POST)
        
        if form.is_valid():
            # Save the main product instance without committing yet
            categorie_service= form.save(commit=False)
            categorie_service.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            categorie_service.save()  # Save product first

          
            
            messages.success(request, " L\'article a été enregistré avec succès.")
            return redirect('compte:categorie_services')
        else:
            messages.error(request, "Erreur lors de l\'enregistrement de la categorie Veuillez vérifier les informations.")
    else:
        form = ServiceCategorieForm()

    return render(request, 'compte/admin/service/add_categorie_service.html', {'form': form})    
##DELETE
@login_required
def categorie_service_delete(request, slug=None):
    categorie_service = get_object_or_404(categories_services, slug=slug)
    
    if request.method == 'POST':
        categorie_service.delete()
        messages.success(request, " La categorie a été supprimé avec succès.")

        return redirect('compte:categorie_services')
        
    # Optionally, you can render a confirmation page here if not using a modal
        # return render(request,'compte/admin/admin.html')

    return redirect('compte:categorie_services')
#

@login_required
def categorie_service_update(request, slug=None):
    categorieService = get_object_or_404(categories_services, slug=slug)
    print("okk")
    if request.method == 'POST':
        form = ServiceCategorieForm(request.POST, request.FILES, instance=categorieService)
        if form.is_valid():
            # Sauvegarde du produit, y compris la photo si un nouveau fichier est téléchargé
            categorieService = form.save(commit=False)
            categorieService.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            categorieService.save()  # Save product first

            messages.success(request, " L\'article a été mis à jour avec succès.")
            return redirect('compte:categorie_services')
        else:
            # Ajout de messages d'erreur spécifiques pour le formulaire
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations saisies.')
    else:
        form = ServiceCategorieForm(instance=categorieService)

    return render(request, 'compte/admin/service/update_categorie_service.html', {'form': form})
################################SERVICES
def service(request):
    if request.user.is_authenticated:
        
        services=Services.objects.all()
        article=Article.objects.all()
        nombre_article=article.count()
        print("nnnn",nombre_article)
        context={
        'service':services,
        'nombre_article':nombre_article,
        }
    else:
        return redirect('compte:login')
    return render(request,'compte/admin/service/service.html',context)
@login_required
def add_service(request):
    if request.method == 'POST':
        # Initialize the form with POST data and files
        form = ServiceForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the main product instance without committing yet
            service = form.save(commit=False)
            service.user = request.user  # Assign the current user

            # Save the product instance to the database
            service.save()  # Save product first

          
            
            messages.success(request, " Le service a été enregistré avec succès.")
            return redirect('compte:service')
        else:
            messages.error(request, "Erreur lors de l\'enregistrement du service Veuillez vérifier les informations.")
    else:
        form = ServiceForm()

    return render(request, 'compte/admin/service/add_service.html', {'form': form})
##

@login_required
def service_update(request, slug=None):
    service = get_object_or_404(Services, slug=slug)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            # Sauvegarde du produit, y compris la photo si un nouveau fichier est téléchargé
            service = form.save(commit=False)
            service.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            service.save()  # Save product first

            messages.success(request, " Le service a été mis à jour avec succès.")
            return redirect('compte:service')
        else:
            # Ajout de messages d'erreur spécifiques pour le formulaire
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations saisies.')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'compte/admin/service/service_update.html', {'form': form})
####
@login_required
def service_delete(request, slug=None):
    service = get_object_or_404(Services, slug=slug)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, " Le service a été supprimé avec succès.")

        return redirect('compte:service')
        
    # Optionally, you can render a confirmation page here if not using a modal
        # return render(request,'compte/admin/admin.html')

    return redirect('compte:service')
#