from django.shortcuts import render
from .models import Article, Articlecategorie, ContactMessage, contact_information,expertise
#
from .forms import NewsLetterForm

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
        "link":"https://www.facebook.com/share/1NwES5h9Zk/",
        'linkedin_link':"https://www.linkedin.com/company/kefc-group-consulting-office-sarl/?lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_companies%3BO5BzPmYwRdSZl3kxBDg3Uw%3D%3D"
    }
    return context
####
def messagerepondu_processor(request):
    message_non_repondu=ContactMessage.objects.filter(repondu=False).count()
    context={
        'nombre_message':message_non_repondu,
    }
    return context
#

def newsletter_form(request):
    context= {
        'newsletter_form': NewsLetterForm()
    }
    return context
#
def contact_entreprise_processor(request):
    contact=contact_information.objects.all()
    print("cccc",contact)
    context = {
        'entreprise_contact':contact
    }
    return context
