import hashlib
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Professeur
from django.core.mail import EmailMessage
from django.conf import settings 
from django.template.loader import render_to_string


@receiver(post_save, sender = Professeur)
def createProfesseur(sender, instance, created, **kwargs):
    if created == True:
        user = instance
        subject = 'Préinscription des professeurs'
        context = {'user': user}
        template = render_to_string("comptes/email_professeur_created.html" , context)
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER]
        )
        email.fail_silently = False
        email.send()
    
     

    

