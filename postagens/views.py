from django.shortcuts import render
from .models import postagem

# Create your views here.

def home(request):
    return render(request, 'home.html')

def post_list(request):
    nome_template= 'home.html'
    posts = postagem.objects.all()
    context={
        'posts': posts
        }
    return render(request, nome_template, context)