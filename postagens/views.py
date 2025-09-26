from django.shortcuts import render, redirect
from .models import postagem, Perfil
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
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
        Titulo= request.POST.get('Título da publicação')
        Descrição= request.POST.get('Descrição do post')
        imagem= request.FILES.get('Imagem do post')
        perfil = Perfil.objects.get(user=request.user)
        if not all([Titulo, Descrição, imagem]):
            return render (request, 'criar_post.html', {'erro': 'Escreva alguma coisa'})  
        novo_post = postagem(titulo=Titulo, descricao=Descrição, imagem=imagem, autor=perfil)
        novo_post.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'criar_post.html')
