from django import forms
from .models import postagem

class PostForm(forms.ModelForm):
    class Meta:
        model=postagem
        fields=['titulo','descricao','imagem']