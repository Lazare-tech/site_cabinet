from django.shortcuts import get_object_or_404, redirect, render

from cabinet.models import Article, Articlecategorie

# Create your views here.
def home(request):
    return render(request,'cabinet/body/index.html')
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
def contacts(request):
    return render(request,'cabinet/body/contact.html')
#
#
def blog(request):
    return render(request,'cabinet/body/blog.html')


# 
def blog (request,slug=None):
    
    if slug:
        categorie = get_object_or_404(Articlecategorie, slug=slug)
        articles_precedents = Article.objects.filter(article=categorie)
        a= Article.objects.filter(slug=slug)
        print("okk",a)
    else:
            # Si aucune catégorie n'est sélectionnée, montrer les articles les plus récents
            articles_precedents = Article.objects.all().order_by('-date_publie')
    
    #categorie article
    
    context = {
        'articles_precedents': articles_precedents,
        'categorie_article': Articlecategorie.objects.all(),
        'article_a_la_une': Article.objects.latest('date_publie')  # Par exemple


    }
    return render(request, 'cabinet/body/blog.html', context)
#
from django.http import JsonResponse
from .models import Article

def article(request, slug=None):
    
    article= get_object_or_404(Article,slug=slug)
        # print("ok",article.slug)
   
    context={
        'article':article,
        'articles_precedents': Article.objects.all().order_by('-date_publie').exclude(slug=slug),
    'categorie_article': Articlecategorie.objects.all(),


    }
    return render(request,'cabinet/body/category-article.html',context)
    