from django.contrib import admin
from django.utils.text import Truncator
from django.utils.html import format_html

from .models import Articlecategorie,Article

# Register your models here.
class ArtcileCategorieAdmin(admin.ModelAdmin):
    list_display=('nom_article','slug')
admin.site.register(Articlecategorie,ArtcileCategorieAdmin)
###

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'afficher_contenu_extrait', 'photo', 'date_publie', 'slug')
    list_filter = ('date_publie',)
    search_fields = ('titre', 'slug')

    def afficher_contenu_extrait(self, obj):
        # Limiter à 30 mots ou à 150 caractères si tu préfères
        extrait = Truncator(obj.contenu).words(7, truncate='...')
        return format_html('<span title="{}">{}</span>', obj.contenu, extrait)

    afficher_contenu_extrait.short_description = 'Extrait de Contenu'

admin.site.register(Article, ArticleAdmin)