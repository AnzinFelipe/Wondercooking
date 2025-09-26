from django.urls import path
from . import views
from .views import LikePostView

urlpatterns = [
    path('', views.home, name = 'home'),
    path('post_detalhe/<int:id>', views.post_detalhe, name = 'post_detalhe'),
    path('accounts/registrar/', views.registrar, name='registrar'),
    path('criar_post/', views.criar_post, name="criar_post"),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
]