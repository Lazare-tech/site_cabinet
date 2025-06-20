from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.conf import settings
from django.views import View

from cabinet.forms import NewsLetterForm
from cabinet.models import Article, Articlecategorie, ContactMessage, News_letter, Services, contact_information, expertise
from compte.models import User
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
#
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm


# from dotenv import load_dotenv
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
# Create your views here.def login_page(request):
##################


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ArticleCategorieForm, ArticleForm, ContactMessageForm, LoginForm, ServiceCategorieForm, ServiceForm, SignupForm, enterprise_contactForm
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
    categorie_ser=expertise.objects.all()
    # #
    article=Article.objects.all()
    nombre_article=article.count()

    context={
        # 'article':article,
        'expertise':categorie_ser,
        'nombre_article':nombre_article,
    }
    return render(request,'compte/admin/service/service_categorie.html',context)
#
def expertise_detail(request, slug):
    expertise_obj = get_object_or_404(expertise, slug=slug)
    return render(request, f"cabinet/body/{slug}.html", {"expertise": expertise_obj})

@login_required
def add_expertise(request):
    if request.method == 'POST':
        # Initialize the form with POST data and files
        form =  ServiceCategorieForm(request.POST)
        
        if form.is_valid():
            # Save the main product instance without committing yet
            expertise= form.save(commit=False)
            expertise.user = request.user  # Assign the current user
            
            # Save the product instance to the database
            expertise.save()  # Save product first

          
            
            messages.success(request, " L\'article a été enregistré avec succès.")
            return redirect('compte:expertises')
        else:
            messages.error(request, "Erreur lors de l\'enregistrement de la categorie Veuillez vérifier les informations.")
    else:
        form = ServiceCategorieForm()

    return render(request, 'compte/admin/service/add_expertise.html', {'form': form})    
##DELETE
@login_required
def expertise_delete(request, slug=None):
    expertis = get_object_or_404(expertise, slug=slug)
    
    if request.method == 'POST':
        expertis.delete()
        messages.success(request, " La categorie a été supprimé avec succès.")

        return redirect('compte:expertises')
        
    # Optionally, you can render a confirmation page here if not using a modal
        # return render(request,'compte/admin/admin.html')

    return redirect('compte:expertises')
#

@login_required
def expertise_update(request, slug=None):
    categorieService = get_object_or_404(expertise, slug=slug)
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
            return redirect('compte:expertises')
        else:
            # Ajout de messages d'erreur spécifiques pour le formulaire
            messages.error(request, 'Une erreur s\'est produite. Veuillez vérifier les informations saisies.')
    else:
        form = ServiceCategorieForm(instance=categorieService)

    return render(request, 'compte/admin/service/update_expertise.html', {'form': form})
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
###################SENT MESSAGE
def confirm_message(request):
    return render(request,'cabinet/body/confirm_message.html')
#

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a bien été envoyé. Nous vous répondrons dans les meilleurs délais.')
            return redirect('compte:confirm_message')  # Redirige vers la page contact ou une page de confirmation
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ContactMessageForm()

    return render(request, 'compte/admin/contact/contact.html', {'form': form})
@login_required
def message(request):
   message = ContactMessage.objects.all().order_by('repondu', '-date_envoi')  # Les non-répondus en haut

   context={
       'message':message,
   }

   return render(request, 'compte/admin/contact/message_contact.html', context)
#
@login_required
def delete_message(request,slug=None):
    message = get_object_or_404(ContactMessage, slug=slug)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, " Le message a été supprimé avec succès.")

        return redirect('compte:message')
        
###
@login_required
def answer_message(request, slug):
    message_obj = get_object_or_404(ContactMessage, slug=slug)

    if request.method == 'POST':
        contenu = request.POST.get('reponse')
        sujet = f"Réponse à votre message: {message_obj.objet}"
        try:
            send_mail(
                sujet,
                contenu,
                settings.EMAIL_HOST_USER,  # expéditeur (tu dois l'importer depuis settings si pas dans ce fichier)
                [message_obj.email],  # destinataire
                fail_silently=False
            )
            message_obj.repondu = True
            message_obj.save()
            messages.success(request, f"Message envoyé à {message_obj.email}")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi: {e}")

    return redirect('compte:message')
  # ou ton nom de vue principale
####
def contact_list(request):
    contacts =contact_information.objects.all()
    return render(request, 'compte/admin/contact/enterprise_contact_list.html', {'entreprise_contact': contacts})
#
@login_required
def contact_create(request):
    form = enterprise_contactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('compte:contact_list')
    return render(request, 'compte/admin/contact/enterprise_create_contact.html', {'form': form})
#
@login_required
def contact_update(request, slug):
    contact = get_object_or_404(contact_information, slug=slug)
    form = enterprise_contactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        messages.success(request, " Le contact a été mis à jour avec succès.")

        return redirect('compte:contact_list')
    return render(request, 'compte/admin/contact/enterprise_update_contact.html', {'form': form})

###
@login_required
def contact_delete(request, slug):
    contact = get_object_or_404(contact_information, slug=slug)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, " Le contact a été supprimer avec succès.")

        return redirect('compte:contact_list')
#
@login_required
def newsletter_list(request):
    new=News_letter.objects.all()
    context={
        'news':new
    }
    return render(request,'compte/admin/newsletter/list_news.html',context)
##
@login_required
def delete_news(request, slug):
    news = get_object_or_404(News_letter, slug=slug)

    if request.method == 'POST':
        news.delete()
        messages.success(request, f"L'email {news.email} a été supprimé avec succès.")
        return redirect('compte:newsletter_list')  # adapte cette URL à celle qui liste les emails
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect('compte:newsletter_list')
#
