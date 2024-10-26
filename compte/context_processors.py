# from django.shortcuts import render
# from .models import Article, Articlecategorie
# #
# def articlecategorie_processor(request):
#     categorie_article= Articlecategorie.objects.all()
#     return {'categorie_article':categorie_article}
# #

# def categories_processor(request):
#     categorie_article=Articlecategorie.objects.all()
#     nombre_categorie_article=categorie_article.count()
#     #
#     article=Article.objects.all()
#     nombre_article=article.count()

#     context={
#         'nombre_categorie_article':nombre_categorie_article,
#         'nombre_article':nombre_article,
#     }

#     return context