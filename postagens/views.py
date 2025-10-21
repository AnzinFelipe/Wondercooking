from django.views import View
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Comentario, postagem, Perfil



@login_required(login_url='/accounts/login/')
def home(request):
    
    posts = postagem.objects.all().order_by('-data')
    contexto = {'posts': posts}
    return render(request, 'home.html', contexto)


def post_detalhe(request, id):
    post = get_object_or_404(postagem, pk=id)
    comentarios = Comentario.objects.filter(postagem=post).order_by("-data")

    contexto = {
        'post': post,
        'comentarios': comentarios,
    }

    if request.method == 'POST':
        if not request.user.is_authenticated:
            
            return redirect(f'/accounts/login/?next={request.path}')

        texto = (request.POST.get('texto') or '').strip()

        
        usuario, _ = Perfil.objects.get_or_create(user=request.user)

        if not texto:
            contexto['erro'] = 'Escreva alguma coisa'
            return render(request, 'post_detalhe.html', contexto)

        Comentario.objects.create(texto=texto, usuario=usuario, postagem=post)
        return redirect('post_detalhe', id=post.id)

    return render(request, 'post_detalhe.html', contexto)


@login_required(login_url='/accounts/login/')
def favoritos(request):
    
    posts = postagem.objects.filter(favoritos=request.user).order_by('-data')
    contexto = {'posts': posts}
    return render(request, 'favoritos.html', contexto)


def registrar(request):
    """
    Registro com suas validações originais:
    - Valida username/senha/email
    - Cria User e Perfil
    - Faz login automático e redireciona para 'home'
      (se preferir: troque 'login(request, user)' por 'return redirect("login")')
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        senha = request.POST.get('senha') or ''
        senhaconfirmar = request.POST.get('senhaconfirmar') or ''
        email = (request.POST.get('email') or '').strip()

        errors = []

        
        if not username:
            errors.append('Nome de usuário é obrigatório')
        elif len(username) < 5:
            errors.append('Nome de usuário deve ter pelo menos 5 caracteres')
        elif User.objects.filter(username=username).exists():
            errors.append('Este nome de usuário já existe')

        if not senha:
            errors.append('Senha é obrigatória')
        elif len(senha) < 8:
            errors.append('Senha deve ter pelo menos 8 caracteres')

        if senha != senhaconfirmar:
            errors.append('As senhas não coincidem')

        if email and User.objects.filter(email=email).exists():
            errors.append('Este email já está em uso')

        if errors:
            return render(request, 'registration/register.html', {
                'errors': errors,
                'username': username,
                'email': email
            })

        try:
            user = User.objects.create_user(
                username=username,
                password=senha,
                email=email
            )
            
            Perfil.objects.get_or_create(user=user)

            
            login(request, user)
            return redirect('home')

        except IntegrityError:
            errors.append('Erro ao criar usuário')
            return render(request, 'registration/register.html', {
                'errors': errors,
                'username': username,
                'email': email
            })

    return render(request, 'registration/register.html')


@login_required(login_url='/accounts/login/')
def criar_post(request):
    if request.method == 'POST':
        Titulo = request.POST.get('Título da publicação') or request.POST.get('titulo')
        Descrição = request.POST.get('Descrição do post') or request.POST.get('descricao')
        imagem = request.FILES.get('Imagem do post') or request.FILES.get('imagem')

        
        perfil = get_object_or_404(Perfil, user=request.user)

        if not all([Titulo, Descrição, imagem]):
            return render(request, 'criar_post.html', {
                'erro': 'Preencha todos os campos (título, descrição e imagem).'
            })

        novo_post = postagem(titulo=Titulo, descricao=Descrição, imagem=imagem, autor=perfil)
        novo_post.save()
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'criar_post.html')


class LikePostView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, post_id):
        post = get_object_or_404(postagem, pk=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('home')


class FavoritePostView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, post_id):
        post = get_object_or_404(postagem, pk=post_id)

        if request.user in post.favoritos.all():
            post.favoritos.remove(request.user)
        else:
            post.favoritos.add(request.user)

        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('home')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username') or ''
        password = request.POST.get('password') or ''
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')

        return render(request, 'registration/login.html', {
            'errors': ['Nome de usuário ou senha incorretos.']
        })

    return render(request, 'registration/login.html')
