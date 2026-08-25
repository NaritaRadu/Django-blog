from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
#deci dam inherit la clasa Model,unde avem deja tabele create
#si fields
class Post(models.Model):
    title=models.CharField(max_length=100)
    #unrestricted text
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    #daca nu setez eu data,se pune una automat
    #daca pun paranteze la now,atunci functia va face actiunea atunci
    #altfel,doar transmit functia
    #am folosit acel atribut pt a primi data postului cand l am postat
    #si poate fi si modificata
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    #el va fi un obiect User
    #ok,asa fac o relatie in care un user poate avea mai multe posts
    #dar nu post poate avea un singur user
    #on delete,practic cand sterg un user,imi sterge si postarea
    
    views=models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.title},{self.author}"
    #va returna reprezentarea unui post
    #returneaza titlul post ului si numele autorului aparent
    #cand dau self.author
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    

#Ce înseamnă ForeignKey? Îi spune bazei de date că fiecare
# comentariu aparține unei anumite postări. Dacă postarea
# este ștearsă, on_delete=models.CASCADE va șterge automat
# și comentariile ei.
    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author=models.CharField(max_length=80)
    body=models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comentariu de la {self.author} la {self.post.title}'