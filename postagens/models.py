from django.db import models

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length = 100, blank = False)

    def __str__(self):
        return self.nome

class Postagens(models.Model):
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    titulo = models.CharField(max_length = 100, blank = False)
    descricao = models.TextField(blank = False)
    data = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.titulo} - Autor: {self.autor}"
