from .models import Post, Perfil, Comentario, Mensaje, CodigoInvitacion
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Post, Perfil, Comentario, Mensaje

def feed(request):
    posts = Post.objects.all().order_by('-fecha')
    return render(request, 'feed.html', {'posts': posts})

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        codigo = request.POST['codigo'].strip()

        try:
            inv = CodigoInvitacion.objects.get(codigo=codigo, usado=False)
        except CodigoInvitacion.DoesNotExist:
            return render(request, 'registro.html', {'error': 'Código de invitación inválido o ya usado.'})

        user = User.objects.create_user(username=username, password=password)
        Perfil.objects.create(usuario=user)
        inv.usado = True
        inv.save()
        login(request, user)
        return redirect('feed')
    return render(request, 'registro.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
    return render(request, 'login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def nuevo_post(request):
    if request.method == 'POST':
        contenido = request.POST['contenido'].strip()
        imagen = request.FILES.get('imagen')
        if contenido or imagen:
            Post.objects.create(usuario=request.user, contenido=contenido, imagen=imagen)
    return redirect('feed')

def eliminar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.usuario:
        post.delete()
    return redirect('feed')

def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('feed')

def perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil = get_object_or_404(Perfil, usuario=usuario)
    posts = Post.objects.filter(usuario=usuario).order_by('-fecha')
    ya_sigue = False
    if request.user.is_authenticated:
        try:
            mi_perfil = Perfil.objects.get(usuario=request.user)
            ya_sigue = usuario in mi_perfil.siguiendo.all()
        except Perfil.DoesNotExist:
            pass
    return render(request, 'perfil.html', {'usuario': usuario, 'perfil': perfil, 'posts': posts, 'ya_sigue': ya_sigue})

def seguir(request, username):
    usuario = get_object_or_404(User, username=username)
    mi_perfil = get_object_or_404(Perfil, usuario=request.user)
    if usuario in mi_perfil.siguiendo.all():
        mi_perfil.siguiendo.remove(usuario)
    else:
        mi_perfil.siguiendo.add(usuario)
    return redirect('perfil', username=username)

def editar_perfil(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    if request.method == 'POST' and request.FILES.get('foto'):
        perfil.foto = request.FILES['foto']
        perfil.save()
    return redirect('perfil', username=request.user.username)

def comentar(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        contenido = request.POST['contenido'].strip()
        if contenido:
            Comentario.objects.create(post=post, usuario=request.user, contenido=contenido)
    return redirect('feed')

def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user == comentario.usuario:
        comentario.delete()
    return redirect('feed')

def buscar(request):
    query = request.GET.get('q', '').strip()
    usuarios = []
    if query:
        usuarios = User.objects.filter(username__icontains=query)
    return render(request, 'buscar.html', {'usuarios': usuarios, 'query': query})

def mensajes(request):
    conversaciones = User.objects.filter(
        mensajes_recibidos__remitente=request.user
    ).distinct() | User.objects.filter(
        mensajes_enviados__destinatario=request.user
    ).distinct()
    return render(request, 'mensajes.html', {'conversaciones': conversaciones})

def conversacion(request, username):
    otro = get_object_or_404(User, username=username)
    msgs = Mensaje.objects.filter(
        remitente=request.user, destinatario=otro
    ) | Mensaje.objects.filter(
        remitente=otro, destinatario=request.user
    )
    msgs = msgs.order_by('fecha')
    Mensaje.objects.filter(remitente=otro, destinatario=request.user, leido=False).update(leido=True)
    if request.method == 'POST':
        contenido = request.POST['contenido'].strip()
        if contenido:
            Mensaje.objects.create(remitente=request.user, destinatario=otro, contenido=contenido)
        return redirect('conversacion', username=username)
    return render(request, 'conversacion.html', {'otro': otro, 'msgs': msgs})