# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Reponse, Statut
    
class ReponseAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'points', 'coef', 'sait_vraiment_pas','question_pas_claire', 'ressources_insuffisantes', 'adresse' )

class StatutAdmin(admin.ModelAdmin):
    list_display = ('label', 'statut')
    
# Register your models here.
admin.site.register(Reponse, ReponseAdmin)
admin.site.register(Statut, StatutAdmin)