from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('mensajes/', views.mensajes, name='mensajes'),
path('mensajes/<str:username>/', views.conversacion, name='conversacion'),
    path('buscar/', views.buscar, name='buscar'),
    path('admin/', admin.site.urls),
    path('', views.feed, name='feed'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('post/', views.nuevo_post, name='nuevo_post'),
    path('like/<int:post_id>/', views.like, name='like'),
    path('eliminar/<int:post_id>/', views.eliminar_post, name='eliminar_post'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('seguir/<str:username>/', views.seguir, name='seguir'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('comentar/<int:post_id>/', views.comentar, name='comentar'),
    path('eliminar-comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)