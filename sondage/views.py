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
    return render(request, 'sondage/index.html')

def form(request, ouiNonSliderValue=50):
    statutResultat = Statut.objects.get(label="resultat").statut
    deactive = False
    
    if not (statutResultat=="active"):
        deactive = True #on indique que c'est suspendu
        form = ReponseForm() #et en plus on remet à zéro le formulaire
        return render (request, 'sondage/form.html', locals())
    elif request.method == 'POST':
        remote_addr = request.META.get("HTTP_X_FORWARDED_FOR")
        try:
            instance = Reponse.objects.get(adresse=remote_addr)
            form = ReponseForm(instance=instance, data=request.POST)
        except Reponse.DoesNotExist:
            form = ReponseForm(request.POST)
            
        if form.is_valid(): #on compte les points
            points = form.cleaned_data['points'] 
            question_pas_claire = form.cleaned_data['question_pas_claire'] 
            ressources_insuffisantes = form.cleaned_data['ressources_insuffisantes'] 
            instance = form.save(commit=False)
            instance.adresse = remote_addr
            instance.save()
            ouiNonSliderValue = instance.points
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
        ratio_oui = 0.0
        ratio_non = 0.0
        ratio_sp = 0.0
        ratio_legitimite = 100
        if not nb_reponses==0:
            for r in result_list:
                if r.question_pas_claire or r.ressources_insuffisantes :
                    total_pas_legitime += 1
                else :
                    nb_suffrage_exprimes += 1
                    total_non += 100-r.points
                    total_oui += r.points
                    #total_sp + = 50-(math.fabs(r.points-50))
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
    