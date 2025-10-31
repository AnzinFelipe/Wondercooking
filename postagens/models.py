from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Use CloudinaryField when Cloudinary is configured; otherwise fallback to ImageField
try:
    if getattr(settings, 'CLOUDINARY_API_KEY', None):
        from cloudinary.models import CloudinaryField
        def _image_field():
            return CloudinaryField('images')
    else:
        raise ImportError()
except Exception:
    def _image_field():
        return models.ImageField(upload_to='images/', blank=True, null=True)

# Create your models here.
class Alergias(models.Model):
    alergia = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.alergia

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    alergia = models.ManyToManyField(Alergias, blank=True)
    def __str__(self):
        return self.user.username

class postagem(models.Model):
    autor = models.ForeignKey(Perfil, on_delete = models.CASCADE)
    titulo = models.CharField(max_length = 100, blank = False)
    descricao = models.TextField(blank = False)
    data = models.DateTimeField("Publicado em: ", auto_now_add = True)
    imagem = _image_field()
    likes = models.ManyToManyField(User, related_name='postagens_likes', blank=True)
    favoritos = models.ManyToManyField(User, related_name='postagens_favoritos', blank=True)
    alergia = models.ManyToManyField(Alergias, blank=True)
    def __str__(self):
        return f"{self.titulo} - Autor: {self.autor}"
    
class HashTag(models.Model):
    hashtagnome = models.CharField(max_length = 50, blank = True, null=True)
    hashtaquant=models.IntegerField(null=True, blank=True)
    post=models.ForeignKey(postagem, on_delete=models.CASCADE, null=True)
    tempo=models.DateTimeField(auto_now_add=True)
    dia=models.DateField(auto_now_add=True)
    hora=models.TimeField(auto_now_add=True)
    user=models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True)

class Comentario(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete = models.CASCADE)
    postagem = models.ForeignKey(postagem, on_delete = models.CASCADE)
    texto = models.TextField(blank = False)
    data = models.DateTimeField("Publicado em: ", auto_now_add = True)

    def __str__(self):
        return f"Comentário de {self.usuario} na postagem: {self.postagem}"
