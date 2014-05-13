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
    if statut == "RAZ" or request.method=='GET':
        return render(request, 'sondage/index.html')
    else:
        return render(request, 'sondage/choiceNb.html')

def choiceNb(request):
    return render(request, 'sondage/choiceNb.html')

def form(request, ouiNonSliderValue=50):
    statutResultat = Statut.objects.get(label="resultat").statut
    deactive = False
    dataForm = {"points":50, "question_pas_claire":False, "ressources_insuffisantes":False, "coef":1}
    if not (statutResultat=="active"):
        deactive = True #on indique que c'est suspendu
        form = ReponseForm(data=dataForm)
        ouiNonSliderValue = 50
        return render(request, 'sondage/form.html', locals())
    if request.method == 'POST':
        remote_addr = request.META.get("HTTP_X_FORWARDED_FOR")
        if "choixCoef" in request.POST: #ça veut dire qu'on arrive de l'accueil
            if request.POST["choixCoef"]=="DEUX":
                dataForm["coef"]=2
        else: #si on vient du form lui-même
            dataForm = request.POST
        try:
            instance = Reponse.objects.get(adresse=remote_addr)
            form = ReponseForm(instance=instance, data=dataForm)
        except Reponse.DoesNotExist:
            form = ReponseForm(dataForm)           
        if form.is_valid(): #on compte les points
            instance = form.save(commit=False)
            instance.adresse = remote_addr
            instance.save()
            ouiNonSliderValue = instance.points
        else:
            probleme = True    
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
            form = ReponseForm(data=dataForm)       
    return render(request, 'sondage/form.html', locals())

def resultats(request):
    statut = Statut.objects.get(label="resultat").statut
    is_blank = False
    if statut == "RAZ":
        is_blank = True
    else:
        result_list = Reponse.objects.all()
        nb_connected = len(result_list)
        nb_reponses = 0
        nb_suffrage_exprimes = 0
        total_oui = 0.0
        total_non = 0.0
        total_homogeneite = 0.0
        total_pas_legitime = 0.0
        ecart_moyenne = 0.0
        ratio_oui = 0.0
        ratio_non = 0.0
        ratio_homogeneite = 0.0
        ratio_legitimite = 100
        if not nb_connected==0:
            for r in result_list:
                nb_reponses += r.coef
                if r.question_pas_claire or r.ressources_insuffisantes :
                    total_pas_legitime += r.coef
                else :
                    nb_suffrage_exprimes += r.coef
                    total_non += (100-r.points)*r.coef
                    total_oui += (r.points)*r.coef
                    #total_sp += 50-(abs(r.points-50))
            ratio_legitimite= int(round(100-total_pas_legitime/nb_reponses*100)) 
            if not nb_suffrage_exprimes==0:
                ratio_oui = int(round(total_oui/nb_suffrage_exprimes))
                ratio_non = int(round(total_non/nb_suffrage_exprimes))
                for r in result_list:
                    ecart_moyenne += abs(((r.points)*r.coef)-ratio_oui)
                ratio_homogeneite = 100-(round(2*ecart_moyenne/nb_suffrage_exprimes))

        
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
    