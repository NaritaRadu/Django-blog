from django.shortcuts import render,get_object_or_404,redirect
#asta face direct legatura cu templates
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
#. inseamna ca e in folderul curent
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CommentForm
from django.views.generic.edit import FormMixin

#acum orice variabila de tip posts va fi accesibila in interiorul
#template ului home
#ultimul arg al functiei render e optional si primeste un dictionar

def home(request):
    context={
        'posts':Post.objects.all() # asa vom putea accesa cheia acestui dictionar
                      # in interiorul template ului
    }
    #acum vom face un query care va incarca postari
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5 #valoare implicita
    
    def get_paginate_by(self, queryset):
        paginate_by=self.request.GET.get('paginate_by')
        if paginate_by and paginate_by.isdigit():
            return int(paginate_by)
        return self.paginate_by
     
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['popular_posts']=Post.objects.order_by('-views')[:3]
        return context
    
class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    
    paginate_by=5
    
    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        

class PostDetailView(DetailView):
    model=Post
    template_name='blog/post_detail.html'
   
    
    def get_succes_url(self):
        return reverse('post-detail',kwargs={'pk':self.object.id})
    
    def get_object(self, queryset =None):
        post= super().get_object(queryset)
        if self.request.user != post.author:
            post.views+=1
            post.save()
        return post
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['form']=CommentForm()
        return context
    
    def post(self,request,*args,**kwargs):
        self.object=self.get_object()
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=self.object
            comment.save()
            return redirect('post-detail',pk=self.object.pk)
        
        
        context=self.get_context_data(object=self.object)
        context['form']=form
        return render(request,self.template_name,context)
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    
    def form_valid(self, form):
        form.instance.author=self.request.user    
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title','content']
    
    def form_valid(self, form):
        form.instance.author=self.request.user    
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    
    def test_func(self):
            post=self.get_object()
            if self.request.user==post.author:
                return True
            return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

#blog->templates->blog->template.html

