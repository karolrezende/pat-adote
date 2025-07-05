from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Postagem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # <-- Adicionado
    valor = models.TextField()
    telefone = models.TextField()
    localizacao = models.TextField()
    descricao = models.TextField()
    foto = models.ImageField(upload_to='postagens/', null=True, blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    adotado = models.BooleanField(default=False)
    def __str__(self):
        return self.valor
    
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Permite valores nulos
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='usuarios/', null=True, blank=True)

    def __str__(self):
        return self.nome
    
class Comentario(models.Model):
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f'Comentário de {self.usuario.username} em {self.postagem.titulo}'


class Adocao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} adotou {self.postagem.descricao[:20]}'
