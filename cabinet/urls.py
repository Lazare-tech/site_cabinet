from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import cabinet.views
# Gestion de l'erreur 404

app_name = "cabinet"

urlpatterns = [
    path('', cabinet.views.home, name='homepage'),
        path('gestion-fiscalite', cabinet.views.fiscalite, name='fiscalite'),
         path('gestion-comptabilite', cabinet.views.comptabilite, name='comptabilite'),
        path('gestion-juridique', cabinet.views.juridique, name='juridique'),
        path('gestion-management', cabinet.views.management, name='management'),
        path('contact', cabinet.views.contacts, name='contact'),
        path('blog', cabinet.views.blog, name='blog'),



 
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)