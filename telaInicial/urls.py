from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('login/', views.login_view, name='login'),
    path('register/', views.cadastro_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('createPost/', views.create_post, name='createPost'),
    path('deletePost/<int:id>/', views.delete_post, name='deletePost'),
    path('adotar/<int:id>/', views.adotar, name='adotar'),
    path('comentar/<int:id>/', views.comentar, name='comentar'),
    path('minhas-adocoes/', views.minhas_adocoes, name='minhas_adocoes'),
    path('perfil/', views.perfil, name='perfil'),
]