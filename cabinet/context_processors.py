from django.shortcuts import render
from .models import Articlecategorie
#
def articlecategorie_processor(request):
    categorie_article= Articlecategorie.objects.all()
    return {'categorie_article':categorie_article}
