from django.dispatch import receiver 
from django.db.models.signals import post_save 
from .models import Profil , User

@receiver(post_save, sender=User)
def create_profil_for_new_user(sender,  **kwargs):
    if  kwargs['created']: 
        Profil.objects.create(user=kwargs['instance'])