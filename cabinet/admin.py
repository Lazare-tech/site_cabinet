from django.contrib import admin
from django.utils.text import Truncator
from django.utils.html import format_html

from .models import Articlecategorie,Article, ContactMessage, categories_services, contact_information

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
#######################       CONTACT
class ContactAdmin(admin.ModelAdmin):
    list_display=('numero_telephone','email','localisation')
admin.site.register(contact_information,ContactAdmin)

#####################    CATEGORIES SERVICES
class CategorieServiceAdmin(admin.ModelAdmin):
    list_display=('categorie_service',)
admin.site.register(categories_services,CategorieServiceAdmin)

# class ServicesAdmin(admin.ModelAdmin):
#     list_display=('')
class MessageAdmin(admin.ModelAdmin):
    list_display=('nom','email','numero_telephone','objet','contenu','date_envoi')
admin.site.register(ContactMessage,MessageAdmin)

# class ServicesAdmin(admin.ModelAdmin):
#     list_display=('')