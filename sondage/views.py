# -*- coding: utf-8 -*-

#from math import fabs

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

from sondage.forms import ReponseForm

from .models import Reponse, Statut

class SondageRedirectView(RedirectView):
    
    def get_redirect_url(self, *arg, **kwargs):
        return reverse("sondage:index")

def index(request):
    statut = Statut.objects.get(label="resultat").statut
    if statut == "BLACK" or request.method=='GET':
        return render(request, 'sondage/index.html')
    else:
        return render(request, 'sondage/choiceNb.html')

def choiceNb(request):
    return render(request, 'sondage/choiceNb.html')

def form(request, ouiNonSliderValue=50):
    statutResultat = Statut.objects.get(label="resultat").statut
    deactive = False
    dataForm = {"points":50, "question_pas_claire":False, "ressources_insuffisantes":False, "coef":1}
    hasVoted = True
    if not (statutResultat=="active"):
        deactive = True #on indique que c'est suspendu
        form = ReponseForm(data=dataForm)
        ouiNonSliderValue = 50
        return render(request, 'sondage/form.html', locals())
    if request.method == 'POST':
        remote_addr = request.META.get("HTTP_X_FORWARDED_FOR")
        if "choixCoef" in request.POST: #ça veut dire qu'on arrive de l'accueil
            hasVoted = False
            if request.POST["choixCoef"]=="DEUX":
                dataForm["coef"]=2
        else: #si on vient du form lui-même
            dataForm = request.POST
        try:
            instance = Reponse.objects.get(adresse=remote_addr)
            form = ReponseForm(instance=instance, data=dataForm)
        except Reponse.DoesNotExist:
            form = ReponseForm(dataForm)           
 #on compte les points
        instance = form.save(commit=False)
        instance.has_voted = hasVoted
        instance.adresse = remote_addr
        instance.save()
        ouiNonSliderValue = instance.points  
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
            form = ReponseForm(data=dataForm)       
    return render(request, 'sondage/form.html', locals())

def resultats(request):
    statut = Statut.objects.get(label="resultat").statut
    is_blank = False
    if statut == "BLACK":
        is_blank = True
    else:
        device_connected = Reponse.objects.all()
        nb_connected = len(device_connected)
        nb_votes = 0 
        nb_voters = 0 # ie nb_votes*coef
        nb_suffrage_exprimes = 0 # ie votes that are not qualifying the question as invalid
        vote_list = list()
        for r in device_connected:
            nb_voters += r.coef
            if r.has_voted:
                nb_votes += r.coef
                vote_list.append(r)
        total_oui = 0.0
        total_non = 0.0
        total_homogeneite = 0.0
        total_pas_legitime = 0.0
        total_pas_clair=0.0
        total_manque_ressource=0.0
        ecart_moyenne = 0.0
        ratio_oui = 0.0
        ratio_non = 0.0
        ratio_homogeneite = 0.0
        ratio_legitimite = 100
        if not nb_votes == 0:
            for r in vote_list:
                if r.question_pas_claire:
                    total_pas_clair += r.coef
                if r.ressources_insuffisantes:
                    total_manque_ressource += r.coef
                if r.question_pas_claire or r.ressources_insuffisantes :
                    total_pas_legitime += r.coef
                else :
                    nb_suffrage_exprimes += r.coef
                    total_non += (100-r.points)*r.coef
                    total_oui += (r.points)*r.coef
                    #total_sp += 50-(abs(r.points-50))
            ratio_legitimite= int(round(100-total_pas_legitime/nb_votes*100))
            ratio_pas_clair = int(round(total_pas_clair/nb_votes*100))
            ratio_manque_ressource = int(round(total_manque_ressource/nb_votes*100))
            if not nb_suffrage_exprimes==0:
                ratio_oui = int(round(total_oui/nb_suffrage_exprimes))
                ratio_non = 100-ratio_oui
                for r in device_connected:
                    if not (r.question_pas_claire or r.ressources_insuffisantes) :
                        ecart_moyenne += abs(((r.points))-ratio_oui)*r.coef
                ratio_homogeneite = int(100-(round(2*ecart_moyenne/nb_suffrage_exprimes)))

        
    return render(request, 'sondage/resultats.html', locals())
     
def redir(request):
    return render(request, 'sondage/redir.html')
    
def control(request):
    statutResultat = Statut.objects.get(label="resultat")
    if request.method == 'POST':
        if request.POST.get('bouton') == "active":
            statutResultat.statut = "active"
        elif request.POST.get('bouton') == "RAZ":
            for r in Reponse.objects.all():
                r.has_voted=False
                r.save()
        elif request.POST.get('bouton') == "pause":
            statutResultat.statut = "pause"
        elif request.POST.get('bouton') == "BLACK":
            for r in Reponse.objects.all():
                r.has_voted=False
                r.save()              
            statutResultat.statut = "BLACK"
        statutResultat.save()
    currentStatus=statutResultat.statut
    return render(request, 'sondage/control.html', locals())
    