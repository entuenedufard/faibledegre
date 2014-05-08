# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from sondage import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^form/$', views.form, name='form'),
    url(r'^form/(?P<ouiNonSliderValue>\d+)$', views.form, name='form'),
    url(r'^resultats/$', views.resultats, name='resultats'),
    url(r'^redir/$', views.redir, name='redir'),
    url(r'^control/$', views.control, name='control'),
)