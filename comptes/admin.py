from django.contrib import admin
from .models import Utilisateur, Tuteur, Eleve, Professeur, Encadrement
# Register your models here.

admin.site.register(Utilisateur)
admin.site.register(Tuteur)
admin.site.register(Eleve)
admin.site.register(Professeur)
admin.site.register(Encadrement)