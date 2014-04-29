# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from sondage.forms import ReponseForm

from .models import Reponse, Statut

vrai = False

def index(request):
    statutResultat = Statut.objects.get(label="resultat").statut
    
    if request.method == 'POST':
        form = ReponseForm(request.POST)
        if not (statutResultat=="active"):
            deactive = True #on ne compte pas les points et on indique que c'est suspendu
            form = ReponseForm() #et en plus on remet à zéro le formulaire
        elif form.is_valid(): 
            points = form.cleaned_data['points'] 
            question_pas_claire = form.cleaned_data['question_pas_claire'] 
            ressources_insuffisantes = form.cleaned_data['ressources_insuffisantes']     
            form.save()
            return render (request, 'sondage/redir.html')
        else:
            probleme = True
    
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
            form = ReponseForm() 
            
    return render(request, 'sondage/index.html', locals())

def resultats(request):
    statut = Statut.objects.get(label="resultat").statut
    is_blank = False
    if statut == "raz":
        is_blank = True
    else:
        result_list = Reponse.objects.all()
        nb_reponses = len(result_list)
        total_oui = 0
        total_non = 0
        for r in result_list:
            if r.points < 0:
                total_non -= r.points
            else:
                total_oui += r.points
        ratio_oui = total_oui/nb_reponses
        ratio_non = total_non/nb_reponses
    return render(request, 'sondage/resultats.html', locals())
     
def redir(request):
    print ("salut on est dans redir et statut = " + statut) 
    return render(request, 'sondage/redir.html')
    
def control(request):
    
    if request.method == 'POST':
        pass
            
    return render(request, 'sondage/control.html', locals())
    