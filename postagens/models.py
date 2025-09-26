from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.username

class postagem(models.Model):
    autor = models.ForeignKey(Perfil, on_delete = models.CASCADE)
    titulo = models.CharField(max_length = 100, blank = False)
    descricao = models.TextField(blank = False)
    data = models.DateTimeField("Publicado em: ", auto_now_add = True)
    imagem = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.titulo} - Autor: {self.autor}"
    
class Comentario(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete = models.CASCADE)
    postagem = models.ForeignKey(postagem, on_delete = models.CASCADE)
    texto = models.TextField(blank = False)
    data = models.DateTimeField("Publicado em: ", auto_now_add = True)

    def __str__(self):
        return f"Comentário de {self.usuario} na postagem: {self.postagem}"
