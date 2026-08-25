from django.contrib import admin
from django.urls import path
from . import views

from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView

#. = current directory, so we are importing views.py from the same directory as urls.py
#functia include proceseaza calea si trimite un empty string
#aici cauta un patern cu empty string si gaseste o cale
#gaseste functia views.home si intra acolo  iar la final face 
#ce zice functia
#nu poti pune direct clase pt views,dar exista metoda 
#as view care face asta 
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/',views.about,name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
#nu mai trebuie nici macar template pt acest update,django face tot