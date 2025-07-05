from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Postagem,Comentario, Adocao,Usuario
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {
                'erro': 'E-mail ou senha incorretos.'
            })

        user_auth = authenticate(request, username=user.username, password=senha)
        if user_auth:
            login(request, user_auth)
            return redirect('feed')
        else:
            return render(request, 'login.html', {
                'erro': 'E-mail ou senha incorretos.'
            })

    return render(request, 'login.html')


def cadastro_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')

        if User.objects.filter(username=nome).exists():
            return render(request, 'register.html', {'erro': 'Nome de usuário já cadastrado.'})

        if senha != senha2:
            return render(request, 'register.html', {'erro': 'As senhas não coincidem.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'erro': 'E-mail já cadastrado.'})

        user = User.objects.create_user(username=nome, email=email, password=senha)
        Usuario.objects.create(user=user, nome=nome)

        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# === Feed / Postagem ===
@login_required
def feed(request):
    posts = Postagem.objects.filter(adotado=False).order_by('-data_hora')
    return render(request, 'feed.html', {'posts': posts, 'usuario': request.user})


@login_required
def create_post(request):
    if request.method == 'POST':
        descricao = request.POST['descricao']
        foto = request.FILES.get('foto')

        Postagem.objects.create(
            usuario=request.user,
            descricao=descricao,
            foto=foto
        )
        return redirect('feed')
    return redirect('feed')


@login_required
def delete_post(request, id):
    post = get_object_or_404(Postagem, id=id)

    if post.usuario == request.user:
        post.delete()
    return redirect('feed')


@login_required
def adotar(request, id):
    post = get_object_or_404(Postagem, id=id)

    Adocao.objects.create(
        usuario=request.user,
        postagem=post
    )

    
    post.adotado = True
    post.save()

    messages.success(request, f'Você adotou o pet do(a) {post.usuario.username}! ❤️')
    return redirect('feed')


@login_required
def minhas_adocoes(request):
    adocoes = Adocao.objects.filter(usuario=request.user).select_related('postagem').order_by('-data_hora')

    return render(request, 'minhas_adocoes.html', {'adocoes': adocoes})

@login_required
def perfil(request):
    usuario, created = Usuario.objects.get_or_create(
        user=request.user,
        defaults={'nome': request.user.username}
    )

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')

        if senha and senha != senha2:
            return render(request, 'perfil.html', {'usuario': usuario, 'erro': 'As senhas não coincidem.'})

        if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            return render(request, 'perfil.html', {'usuario': usuario, 'erro': 'E-mail já cadastrado por outro usuário.'})

        usuario.nome = nome
        usuario.user.email = email

        
        usuario.user.username = nome

        if senha:
            usuario.user.set_password(senha)

        usuario.user.save()
        usuario.save()

        return redirect('perfil')

    return render(request, 'perfil.html', {'usuario': usuario})

@login_required
def comentar(request, id):
    postagem = get_object_or_404(Postagem, id=id)

    if request.method == 'POST':
        texto = request.POST.get('texto')
        if texto.strip():
            Comentario.objects.create(
                postagem=postagem,
                usuario=request.user,
                texto=texto
            )
    
    return redirect('feed')
    