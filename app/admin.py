from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Formato)
admin.site.register(Conversao)
admin.site.register(Feedback)
admin.site.register(Arquivo)