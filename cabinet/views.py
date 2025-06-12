from django.shortcuts import get_object_or_404, redirect, render

from cabinet.models import Article, Articlecategorie

# Create your views here.
def home(request):
    service=Services.objects.all()
    categories_service=expertise.objects.all()
    articles=Article.objects.order_by('-date_publie')[:2]
    print("aaaa",articles)

    context={
        'service':service,
                'categorie_service':categories_service,
                'articles':articles,

    }
    return render(request,'cabinet/body/index.html',context)
#
def fiscalite(request):
    return render(request,'cabinet/body/fiscalite.html')
#
def comptabilite(request):
    return render(request,'cabinet/body/comptabilite.html')
#
def juridique(request):
    return render(request,'cabinet/body/juridique.html')
#
def management(request):
    return render(request,'cabinet/body/management.html')
#
def nav(request):
    categories_service=expertise.objects.all()
    print("caaaaa",categories_service)
    context={
        'categorie_service':categories_service
    }
    return render(request,'cabinet/navbar/navbar.html',context)

def blog(request,slug=None):
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
    }
    return render(request,'cabinet/body/blog.html',context)


# 
def blog_article (request,slug=None):
    article_a_la_une= Article.objects.latest('date_publie') 

    if slug:
        categorie = get_object_or_404(Articlecategorie, slug=slug)

        articles_precedents = Article.objects.filter(article=categorie)

        print("aaaaa",articles_precedents)
    else:
            # Si aucune catégorie n'est sélectionnée, montrer les articles les plus récents
            articles_precedents = Article.objects.all().order_by('-date_publie').exclude(slug=article_a_la_une.slug)

    #categorie article
    
    context = {
        'articles_precedents': articles_precedents,
        'article_a_la_une': article_a_la_une,  # Par exemple
        'categorie':categorie,

    }
    return render(request, 'cabinet/body/blog.html', context)
#
from django.http import JsonResponse
from .models import Article, Services, expertise

def article(request, slug=None):

    article= get_object_or_404(Article,slug=slug)
    article_a_la= Article.objects.latest('date_publie') 
    article_a_la_une=None
    if article == article_a_la:
        article_a_la_une=article

        
    context={
        'article':article,
        'articles_precedents': Article.objects.all().order_by('-date_publie').exclude(slug=slug),
        'article_a_la_une':article_a_la_une
    }
    return render(request,'cabinet/body/category-article.html',context)
    