from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
import compte.views
#

# path('',LoginView.as_view(template_name='compte/login.html',
#                           redirect_authenticated=True),
#      name='login'),
# path('logout/',LogoutView.as_view(),name='logout')
app_name= "compte"
urlpatterns = [
    path('login/',compte.views.login_page,name='login'),
    path('signup/',compte.views.signup_page,name='signup'),
    path('logout/',compte.views.logout_user,name='logout'),
    path('delete_account',compte.views.delete_account,name='delete_account'),
    path('profile',compte.views.profile_view,name='profile'),
    path('dashboard/',compte.views.dashboard_admin,name='dashboard'),
    ##ARTICLE
        path('add-article/', compte.views.add_article, name='add_article'),
        path('<slug:slug>/update/', compte.views.article_update, name='update_article'),
        path('<slug:slug>/delete/', compte.views.article_delete, name='delete_article'),
    #CATEGORIE ARTICLE
    path('categorie_article',compte.views.article_categorie,name='article'),
    path('add_categorie_article/',compte.views.add_categorie_article,name='add_categorie_article'),
    path('<slug:slug>/article_categoriedelete/', compte.views.categorie_article_delete, name='delete_categorie_article'),
    path('<slug:slug>/article_categorieupdate/', compte.views.categorie_article_update, name='update_categorie_article'),

#CATEGORIES EXPERTISES
# urls.py
path('gestion/<slug:slug>/', compte.views.expertise_detail, name='expertise_detail'),

path('expertise',compte.views.service_categorie,name='expertises'),
path('<slug:slug>/expertise_delete/', compte.views.expertise_delete, name='delete_expertise'),
path('add_expertise/',compte.views.add_expertise,name='add_expertise'),
path('<slug:slug>/expertise_update/', compte.views.expertise_update, name='update_expertise'),
#SERVICES
path('services/', compte.views.service, name='service'),
path('<slug:slug>/service_update/', compte.views.service_update, name='update_service'),
path('<slug:slug>/service_delete/', compte.views.service_delete, name='delete_service'),
 path('add-service/', compte.views.add_service, name='add_service'),

#MESSAGES
path('contact/', compte.views.contact, name='contact'),
path('confirmation_message/', compte.views.confirm_message, name='confirm_message'),
   path('message/', compte.views.message, name='message'),
   path('<slug:slug>/message_delete/', compte.views.delete_message, name='delete_message'),


]
