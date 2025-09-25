from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('post_detalhe/<int:id>', views.post_detalhe, name = 'post_detalhe'),
    path('registrar/', views.registrar, name='registrar'),
]