from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Article, News_letter

@receiver(post_save, sender=Article)
def envoyer_article_aux_newsletters(sender, instance, created, **kwargs):
    if created:  # on envoie uniquement à la création de l'article
        print("SIGNAL ACTIVÉ : article créé")
        sujet = f"📰 Nouvel article publié : {instance.titre}"
        message_html = render_to_string("cabinet/body/newsletter_article.html", {"article": instance})
        liste_emails = News_letter.objects.values_list('email', flat=True)

        for email in liste_emails:
            send_mail(
                sujet,
                "",  # corps texte vide, car on envoie du HTML
                settings.EMAIL_HOST_USER ,
                [email],
                fail_silently=False,
                html_message=message_html
            )
