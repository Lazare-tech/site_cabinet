from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field  # Correct import for CKEditor 5
from bs4 import BeautifulSoup
# Modèle pour les catégories d'articles
class Articlecategorie(models.Model):
    nom_article = models.CharField(max_length=255, verbose_name="Nom de l'article")
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    
    class Meta:
        verbose_name= "Categorie d'article"
        verbose_name_plural= "Categories d'article"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.nom_article)
        unique_slug = slug
        num = 1
        while Articlecategorie.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.nom_article
# Modèle pour les articles individuels
class Article(models.Model):
    article = models.ForeignKey(Articlecategorie, related_name='articles', verbose_name="Article", on_delete=models.CASCADE)
    titre = models.CharField(max_length=255, verbose_name="Titre de l'article", null=True)
    contenu = CKEditor5Field(config_name='extends')  # Use CKEditor5Field here
    photo = models.ImageField(upload_to='article_image', verbose_name="Image de l'article", null=True, blank=True)
    date_publie = models.DateTimeField(verbose_name="Date de publication de l'article", auto_now=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        
    def clean_styles(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup.find_all(True):
            if tag.has_attr("style"):
                styles = tag["style"].split(";")
                filtered_styles = [s for s in styles if not s.strip().startswith("color")]
                tag["style"] = ";".join(filtered_styles).strip()
                if not tag["style"]:
                    del tag["style"]
        return str(soup)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.titre)
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.titre
#
class contact_information(models.Model):
    nom_entreprise=models.CharField(verbose_name="Nom de l\'entreprise ",max_length=255)

    numero_telephone=models.CharField(verbose_name="Numero de telephone",max_length=255)
    email=models.EmailField(verbose_name="Email entreprise")
    localisation=models.CharField(verbose_name="Localisation de l\'entreprise ",max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Informations de contacts'
        verbose_name_plural = 'nformations de contacts'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.email)
        unique_slug = slug
        num = 1
        while contact_information.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.email
# #
class ContactMessage(models.Model):
    nom = models.CharField(verbose_name="Nom et prénom", max_length=255)
    objet = models.CharField(verbose_name="Objet du message", max_length=255)
    numero_telephone = models.CharField(verbose_name="Numéro de téléphone", max_length=255)
    email = models.EmailField(verbose_name="Email de l'entreprise")
    contenu = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(verbose_name="Date d'envoi", auto_now=True)
    repondu = models.BooleanField(verbose_name="Message répondu ?", default=False)  # 
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.email)
        unique_slug = slug
        num = 1
        while ContactMessage.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def __str__(self):
        return self.email

####################CATEGORIES SERVICES
class expertise(models.Model):
    expertise=models.CharField(max_length=255,verbose_name="Expertise")
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Categorie d\'expertise'
        verbose_name_plural = 'Categorie  d\'expertise'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.expertise)
        if expertise.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            raise ValueError(f"Le slug '{slug}' existe déjà. Choisissez une autre valeur pour l'expertise.")
        return slug

    
    def __str__(self):
        return self.expertise
##################SERVICES
class Services(models.Model):
    image_service=models.ImageField(upload_to='Images_des_services',verbose_name="Image du service")
    nom_service=models.ForeignKey(expertise, verbose_name=("Nom de l\'expertise "), on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Service'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.nom_service)
        unique_slug = slug
        num = 1
        while Services.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.nom_service
#
class News_letter(models.Model):
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    email = models.EmailField(verbose_name="Email de l'utilisateur",unique=True)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Date d\inscription de l\'utilisateur ')
    
    class Meta:
        verbose_name = 'News letter'
        verbose_name_plural = 'News letter'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        slug = slugify(self.email)
        unique_slug = slug
        num = 1
        while News_letter.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug
    
    def __str__(self):
        return self.email
#
class  HeroImage (models.Model):
    page=models.CharField(max_length=100,unique=True)
    image=models.ImageField(upload_to='hero_images/')
    alt_text=models.CharField(max_length=255,blank=True)
    titre=models.CharField(max_length=255,blank=True,null=True)
    text_hero=models.TextField(blank=True,null=True)
    
    def __str_(self):
        return f"Hero pour {self.page}"