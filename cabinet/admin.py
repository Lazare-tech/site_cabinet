from django.contrib import admin
from django.utils.text import Truncator
from django.utils.html import format_html

from .models import Articlecategorie,Article, ContactMessage, News_letter, Services, expertise, expertise

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

#####################    CATEGORIES SERVICES
class ExpertiseAdmin(admin.ModelAdmin):
    list_display=('expertise',)
admin.site.register(expertise,ExpertiseAdmin)

# 

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('nom_service', 'slug', 'image_tag')
    search_fields = ('nom_service__nom',)  # si `expertise` a un champ `nom`
    readonly_fields = ('slug',)
    
    def image_tag(self, obj):
        if obj.image_service:
            return f'<img src="{obj.image_service.url}" width="60" height="60" style="object-fit:cover;" />'
        return "Pas d'image"
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True  # Pour Django < 2.0 uniquement ; ignoré sinon

@admin.register(News_letter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'slug')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'slug')
#####

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'objet', 'numero_telephone', 'date_envoi', 'repondu')
    search_fields = ('nom', 'email', 'objet', 'contenu')
    list_filter = ('repondu', 'date_envoi')
    readonly_fields = ('slug', 'date_envoi')
    list_editable = ('repondu',)
    ordering = ('-date_envoi',)