# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError


def validate_points(value):
    if value < -100 or value > 100:
        raise ValidationError(u'%s est pas compris entre -100 et 100, benêt' % value)

class Reponse(models.Model):
    """
    Une réponse c'est une réponse de quelqu'un bon voilà quoi
    """
    has_voted = models.BooleanField()
    points = models.IntegerField(default=0, validators=[validate_points])
    timestamp = models.DateTimeField(auto_now_add=True)
    biased_question = models.BooleanField()
    question_pas_claire = models.BooleanField()
    ressources_insuffisantes = models.BooleanField()
    adresse = models.IPAddressField(null=True, blank=True)
    coef = models.IntegerField(default=1)
    
class Statut(models.Model):
    """
    Alors ici c'est bien pourri mais on stocke le label 
    du statut (genre statut de l'affichage des résultat - actif, désactivé ou
    remis à zéro) et le statut afférent, par exemple activé, desactivé ou RAZ
    """
    label = models.CharField(max_length=200)
    statut = models.CharField(max_length=200)


