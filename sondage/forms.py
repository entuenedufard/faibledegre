#-*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from models import Reponse

class ReponseForm(forms.ModelForm): 
    class Meta:
        model = Reponse
        exclude = ('timestamp',)