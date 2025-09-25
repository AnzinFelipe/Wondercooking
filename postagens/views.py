from django.shortcuts import render
from .models import postagem

# Create your views here.

def home(request):
    return render(request, 'home.html')

def home(request):
    posts = postagem.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'home.html', context)