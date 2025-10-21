from django.urls import path
from . import views
from .views import LikePostView, FavoritePostView

urlpatterns = [
    
    path('', views.home, name='home'),

    
    path('registrar/', views.registrar, name='registrar'),

    
    path('criar_post/', views.criar_post, name='criar_post'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('post_detalhe/<int:id>/', views.post_detalhe, name='post_detalhe'),

    
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('favorite/<int:post_id>/', FavoritePostView.as_view(), name='favorite_post'),
]
