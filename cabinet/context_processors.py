from django.shortcuts import render
from .models import Article, Articlecategorie, ContactMessage,expertise
#
def  expertise_processor(request):
    categorie_expertise=expertise.objects.all()
    context={
        'categorie_expertise':categorie_expertise
    }
    return context
#
def articlecategorie_processor(request):
    categorie_article= Articlecategorie.objects.all()
    return {'categorie_article':categorie_article}
#

def categories_processor(request):
    categorie_article=Articlecategorie.objects.all()
    nombre_categorie_article=categorie_article.count()
    #
    article=Article.objects.all()
    nombre_article=article.count()

    context={
        'nombre_categorie_article':nombre_categorie_article,
        'nombre_article':nombre_article,
    }

    return context
###
def contact_whatsapp_processor(request):
    context={
        'number': "22677938213",
        "link":"https://www.facebook.com/share/1NwES5h9Zk/"
    }
    return context
####
def messagerepondu_processor(request):
    message_non_repondu=ContactMessage.objects.filter(repondu=False).count()
    context={
        'nombre_message':message_non_repondu,
    }
    return context