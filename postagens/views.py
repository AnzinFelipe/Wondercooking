from django.views import View
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Comentario, postagem, Perfil
from .models import Comentario, postagem, Perfil, HashTag
import re
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta

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
        try:
            descricao_text = Descrição or ''
            hashtags_field = request.POST.get('hashtags', '') or ''


            found_desc = re.findall(r'#([^\s#.,;:!?)\]\[]+)', descricao_text)

            found_field = re.findall(r'#?([A-Za-z0-9_-]+)', hashtags_field)

            all_tags = set([t.strip().lower() for t in found_desc if t.strip()]) | set([t.strip().lower() for t in found_field if t.strip()])

            for tag in all_tags:
                if not tag:
                    continue
                count_desc = len(re.findall(rf'#({re.escape(tag)})', descricao_text, flags=re.IGNORECASE))
                total_count = count_desc if count_desc > 0 else 1
                obj, created = HashTag.objects.get_or_create(hashtagnome=tag, post=novo_post, defaults={
                    'hashtaquant': total_count,
                    'user': perfil
                })
                if not created:
                    obj.hashtaquant = max(obj.hashtaquant or 0, total_count)
                    obj.save()
        except Exception:
            pass
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

def tags(request, tag):
    posts = postagem.objects.filter(hashtag__hashtagnome__iexact=tag).distinct()
    contexto = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'tag.html', contexto)


def destaques(request):
    if not request.user.is_authenticated:
        return redirect('registrar')

    ultimasemana = timezone.now() - timedelta(days=7)

    posts = postagem.objects.filter(data__gte=ultimasemana).annotate(likes_count=models.Count('likes')).order_by('-likes_count')

    contexto = {
        'posts': posts
    }
    return render(request, 'destaques.html', contexto)