from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field  # Correct import for CKEditor 5

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
