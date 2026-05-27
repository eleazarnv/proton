from django.contrib import admin
from .models import Post, Perfil, Comentario, Mensaje, CodigoInvitacion

admin.site.register(Post)
admin.site.register(Perfil)
admin.site.register(Comentario)
admin.site.register(Mensaje)
admin.site.register(CodigoInvitacion)