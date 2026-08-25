from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#deci primim un sender user si un semnal post_save
#cand un user este saved,atunci trimite semnalul post_save
#acel semnal va fi primit de acel receiver,iac acel receiver
#este de fapt acel create profile.functia primeste instanta userului
#si faptul ca a fost creat,si daca a fost creat,atunci poate crea
#un profile object 
#asa se face in django

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
        instance.profile.save()