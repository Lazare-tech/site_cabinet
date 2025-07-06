from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import cabinet.views
# Gestion de l'erreur 404

app_name = "cabinet"

urlpatterns = [
    path('', cabinet.views.home, name='homepage'),
        path('fiscalite/', cabinet.views.fiscalite, name='fiscalite'),
         path('comptabilite/', cabinet.views.comptabilite, name='comptabilite'),
        path('juridique/', cabinet.views.juridique, name='juridique'),
        path('management/', cabinet.views.management, name='management'),
            path('blog/', cabinet.views.blog, name='blog'),

    path('blog/categorie/<slug:slug>/', cabinet.views.blog_article, name='blog-categorie'),  # Pour la catégorie sélectionnée

        path('blog/article/<slug:slug>/', cabinet.views.article, name='article'),
path('newsletter/', cabinet.views.newsletter_signup, name='newsletters_signup'),

 
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
