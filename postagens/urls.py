from django.urls import path
from . import views
from .views import LikePostView, FavoritePostView

urlpatterns = [
    path('', views.home, name = 'home'),
    path('post_detalhe/<int:id>', views.post_detalhe, name = 'post_detalhe'),
    path('accounts/registrar/', views.registrar, name='registrar'),
    path('registrar/', views.registrar, name='registrar'),
    path('criar_post/', views.criar_post, name="criar_post"),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('favorite/<int:post_id>/', FavoritePostView.as_view(), name='favorite_post'),
    path('tags/<str:tag>/', views.tags, name='tags'),
    path('destaques/', views.destaques, name='destaques'),
    path('perfil/', views.perfil, name='perfil'),
]
