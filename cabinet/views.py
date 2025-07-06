from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render

from cabinet.models import Article, Articlecategorie
from cabinet.forms import NewsLetterForm

# Create your views here.
from django.contrib import messages
from django.db import IntegrityError

def home(request):
    service = Services.objects.all()
    categories_service = expertise.objects.all()
    articles = Article.objects.order_by('-date_publie')[:2]
    categorie_article = Articlecategorie.objects.all()
    heros = HeroImage.objects.filter(page='acceuil').order_by('id')
   
    context = {
        'service': service,
        'categorie_service': categories_service,
        'articles': articles,
        'categorie_article': categorie_article,
        'heros':heros,
    }

    return render(request, 'cabinet/body/index.html', context)
#

def fiscalite(request):
    hero = HeroImage.objects.filter(page='fiscalite').first()

    return render(request,'cabinet/body/fiscalite.html',{'hero':hero})

def juridique(request):
    hero = HeroImage.objects.filter(page='juridique').first()

    return render(request,'cabinet/body/juridique.html',{'hero':hero})
#

def management(request):
    hero = HeroImage.objects.filter(page='management').first()

    return render(request,'cabinet/body/management.html',{'hero':hero})

def comptabilite(request):
    hero = HeroImage.objects.filter(page='comptabilite').first()

    return render(request,'cabinet/body/comptabilite.html',{'hero':hero})
#
def nav(request):
    categories_service=expertise.objects.all()
    print("caaaaa",categories_service)
    context={
        'categorie_service':categories_service
    }
    return render(request,'cabinet/navbar/navbar.html',context)

def blog(request,slug=None):
    hero=HeroImage.objects.filter(page='blog').first()

    article_a_la_une= Article.objects.latest('date_publie') 
    articles_precedents = Article.objects.all().order_by('-date_publie').exclude(slug=article_a_la_une.slug)
    #
    categorie=None
    if slug:
        categorie = Articlecategorie.objects.all()

    context={
            'articles_precedents': articles_precedents,
        'article_a_la_une': article_a_la_une,  # Par exemple
        'categorie':categorie,
        'hero':hero
    }
    return render(request,'cabinet/body/blog.html',context)


# 
def blog_article (request,slug=None):
    hero=HeroImage.objects.filter(page='blog').first()

    article_a_la_une= Article.objects.latest('date_publie') 

    if slug:
        categorie = get_object_or_404(Articlecategorie, slug=slug)


        articles_precedents = Article.objects.filter(article=categorie)

    else:
            # Si aucune catégorie n'est sélectionnée, montrer les articles les plus récents
            articles_precedents = Article.objects.all().order_by('-date_publie').exclude(slug=article_a_la_une.slug)

    #categorie article

    context = {
        'articles_precedents': articles_precedents,
        'article_a_la_une': article_a_la_une,  # Par exemple
        'categorie':categorie,
        'hero':hero,

    }
    return render(request, 'cabinet/body/blog.html', context)
#
from django.http import JsonResponse
from .models import Article, HeroImage, Services, expertise

def article(request, slug=None):
    hero=HeroImage.objects.filter(page='blog').first()

    article= get_object_or_404(Article,slug=slug)
    article_a_la= Article.objects.latest('date_publie') 
    article_a_la_une=None
    if article == article_a_la:
        article_a_la_une=article

        
    context={
        'article':article,
        'articles_precedents': Article.objects.all().order_by('-date_publie').exclude(slug=slug),
        'article_a_la_une':article_a_la_une,
        'hero':hero,
    }
    return render(request,'cabinet/body/category-article.html',context)
##
from urllib.parse import urlparse, urlunparse

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                form.save()
                messages.success(request, "✅ Merci pour votre inscription à la newsletter !")
            except IntegrityError:
                messages.error(request, "⚠️ Cette adresse email est déjà inscrite.")
        else:
            if form.errors.get('email'):
                messages.error(request, f"❌ Erreur sur le champ email : {form.errors['email'][0]}")
            else:
                messages.error(request, "❌ Une erreur est survenue. Veuillez vérifier le formulaire.")
    
    # Nettoyer l'URL avant d'ajouter #newsletter
    referer = request.META.get('HTTP_REFERER', '/')
    parsed = urlparse(referer)
    cleaned_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    return redirect(cleaned_url + '#newsletter')
