from django.shortcuts import render, redirect
from .models import postagem, Perfil
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.

def home(request):
    posts = postagem.objects.all()
    contexto = {
        'posts': posts
    }
    return render(request, 'home.html', contexto)

def post_detalhe(request, id):
    post = postagem.objects.get(pk = id)
    contexto = {
        'post' : post
    }
    return render(request, 'post_detalhe.html', contexto)

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.autor = Perfil.objects.get(user=request.user)
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
    
    return render(request, 'criar_post.html', {'form': form})