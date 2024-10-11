from django.contrib import admin
from .models import Articlecategorie,Article
# Register your models here.
class ArtcileCategorieAdmin(admin.ModelAdmin):
    list_display=('nom_article','slug')
admin.site.register(Articlecategorie,ArtcileCategorieAdmin)
###
class ArticleAdmin(admin.ModelAdmin):
    list_display=('article','titre','contenu','photo','date_publie','slug')
admin.site.register(Article,ArticleAdmin)