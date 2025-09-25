from django.shortcuts import render, redirect
from .models import postagem
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

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
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

