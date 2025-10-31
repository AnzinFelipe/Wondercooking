from django.contrib import admin
from .models import Perfil, postagem, Comentario, Alergias, HashTag

# Register your models here.

admin.site.register(Alergias)
admin.site.register(Perfil)
admin.site.register(postagem)
admin.site.register(Comentario)
admin.site.register(HashTag)