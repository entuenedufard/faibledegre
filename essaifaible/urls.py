from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'essaifaible.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^sondage/', include('sondage.urls', namespace="sondage")),
    url(r'^admin/', include(admin.site.urls)),
)
