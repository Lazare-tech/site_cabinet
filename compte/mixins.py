from django.shortcuts import render
from cabinet.models import Article, Articlecategorie



class GlobalData:
    def get_global_data(self, **kwargs):
        categorie_article = Articlecategorie.objects.all()
        nombre_categorie_article = categorie_article.count()

        article = Article.objects.all()
        nombre_article = article.count()

        context = {
            'nombre_categorie_article': nombre_categorie_article,
            'nombre_article': nombre_article,
        }
        return context

    def render_with_global_data(self, request, template_name, context=None):
        if context is None:
            context = {}
        context.update(self.get_global_data())
        return render(request, template_name, context)