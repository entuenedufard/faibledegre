# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from sondage.forms import ReponseForm

from .models import Reponse, Statut

def index(request):
    return render(request, 'sondage/index.html')

def form(request, ouiNonSliderValue=5):
    statutResultat = Statut.objects.get(label="resultat").statut
    deactive = False
    if not (statutResultat=="active"):
        deactive = True #on indique que c'est suspendu
        form = ReponseForm() #et en plus on remet à zéro le formulaire
        return render (request, 'sondage/index.html', locals())
    elif request.method == 'POST':
        form = ReponseForm(request.POST)
        if form.is_valid(): #on compte les points
            points = form.cleaned_data['points'] 
            question_pas_claire = form.cleaned_data['question_pas_claire'] 
            ressources_insuffisantes = form.cleaned_data['ressources_insuffisantes'] 
            form.save()
            form = ReponseForm()  
        else:
            probleme = True    
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
            form = ReponseForm()       
    return render(request, 'sondage/form.html', locals())

def resultats(request):
    statut = Statut.objects.get(label="resultat").statut
    is_blank = False
    if statut == "RAZ":
        is_blank = True
    else:
        result_list = Reponse.objects.all()
        nb_reponses = len(result_list)
        nb_suffrage_exprimes = 0
        total_oui = 0
        total_non = 0
        total_sp = 0
        total_pas_legitime = 0.0
        ratio_oui = 0
        ratio_non = 0
        ratio_sp = 0
        ratio_legitimite = 100
        if not nb_reponses==0:
            for r in result_list:
                if r.question_pas_claire or r.ressources_insuffisantes :
                    total_pas_legitime += 1
                else :
                    nb_suffrage_exprimes += 1
                    if r.points < 0:
                        total_non += -r.points
                        total_sp += 100 + r.points 
                    else:
                        total_oui += r.points
                        total_sp += 100 - r.points
            ratio_oui = total_oui/nb_suffrage_exprimes
            ratio_non = total_non/nb_suffrage_exprimes
            ratio_sp = total_sp/nb_suffrage_exprimes
            ratio_legitimite= round(100-total_pas_legitime/nb_reponses*100)
    return render(request, 'sondage/resultats.html', locals())
     
def redir(request):
    return render(request, 'sondage/redir.html')
    
def control(request):
    statutResultat = Statut.objects.get(label="resultat")
    if request.method == 'POST':
        print (request.POST.get('bouton'))
        if request.POST.get('bouton') == "active":
            statutResultat.statut = "active"
        elif request.POST.get('bouton') == "desactive":
            statutResultat.statut = "desactive"
        elif request.POST.get('bouton') == "RAZ":
            Reponse.objects.all().delete()
            statutResultat.statut = "RAZ"
        statutResultat.save()
    return render(request, 'sondage/control.html', locals())
    