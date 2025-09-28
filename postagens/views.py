from django.views import View
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Comentario, postagem, Perfil
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('registrar')
    posts = postagem.objects.all()
    contexto = {
        'posts': posts
    }
    return render(request, 'home.html', contexto)

def post_detalhe(request, id):
    post = postagem.objects.get(pk = id)
    comentarios = Comentario.objects.filter(postagem = post).order_by("-data")
    contexto = {
        'post' : post,
        'comentarios' : comentarios,
    }
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/accounts/login/?next=' + request.path)
        texto = request.POST.get('texto')
        usuario = Perfil.objects.get(user = request.user)
        post_comentario = post

        if not texto:
            return render (request, 'post_detalhe.html', {'erro': 'Escreva alguma coisa'}) 
        novo_comentario = Comentario(texto = texto, usuario = usuario, postagem = post_comentario)
        novo_comentario.save()
        return redirect('home')  
    return render(request, 'post_detalhe.html', contexto)
@login_required
def favoritos(request):
    posts = postagem.objects.all()
    contexto = {
        'posts': posts
    }
    return render(request, 'favoritos.html', contexto)


def registrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        senhaconfirmar = request.POST.get('senhaconfirmar')
        email = request.POST.get('email', '')
        erros = []
        if not username:
            erros.append('Nome de usuário é obrigatório')
        elif len(username) < 5:
            erros.append('Nome de usuário deve ter pelo menos 5 caracteres')
        elif User.objects.filter(username=username).exists():
            erros.append('Este nome de usuário já existe')
        if not senha:
            erros.append('Senha é obrigatória')
        elif len(senha) < 8:
            erros.append('Senha deve ter pelo menos 8 caracteres')
        
        if senha != senhaconfirmar:
            erros.append('As senhas não coincidem')
        
        if email and User.objects.filter(email=email).exists():
            erros.append('Este email já está em uso')
        if not erros:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=senha,
                    email=email
                )
                Perfil.objects.create(user=user)
                user = authenticate(request, username=username, password=senha)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    erros.append('Erro ao fazer login')
                    
            except IntegrityError:
                erros.append('Erro ao criar usuário')
        if erros:
            return render(request, 'registration/register.html', {
                'errors': erros,
                'username': username,
                'email': email
            })
    else:
        return render(request, 'registration/register.html')

@login_required(login_url='/accounts/login/')
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

    
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(postagem, pk=post_id)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user) 
        return redirect('home')
    
class FavoritePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(postagem, pk=post_id)
        
        if request.user in post.favoritos.all():
            post.favoritos.remove(request.user)
        else:

            post.favoritos.add(request.user) 
        return redirect('home')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'errors': ['Nome de usuário ou senha incorretos.']
            })
    return render(request, 'login.html')