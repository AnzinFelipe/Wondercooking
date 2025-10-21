from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username if self.user else "Usuário sem perfil"


class postagem(models.Model):
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100, blank=False)
    descricao = models.TextField(blank=False)
    data = models.DateTimeField("Publicado em:", auto_now_add=True)
    imagem = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='postagens_likes', blank=True)
    favoritos = models.ManyToManyField(User, related_name='postagens_favoritos', blank=True)

    def __str__(self):
        autor_nome = self.autor.user.username if self.autor and self.autor.user else "Anônimo"
        return f"{self.titulo} - Autor: {autor_nome}"


class Comentario(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    postagem = models.ForeignKey(postagem, on_delete=models.CASCADE)
    texto = models.TextField(blank=False)
    data = models.DateTimeField("Publicado em:", auto_now_add=True)

    def __str__(self):
        usuario_nome = self.usuario.user.username if self.usuario and self.usuario.user else "Usuário desconhecido"
        return f"Comentário de {usuario_nome} na postagem: {self.postagem.titulo if self.postagem else 'Sem título'}"
