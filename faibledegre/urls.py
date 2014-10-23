
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

import socketio.sdjango

from sondage.views import SondageRedirectView

from django.contrib import admin
admin.autodiscover()
socketio.sdjango.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'faibledegre.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^socket\.io', include(socketio.sdjango.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', SondageRedirectView.as_view() ),
    
)

urlpatterns += i18n_patterns('',
    # Examples:
    # url(r'^$', 'faibledegre.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^sondage/', include('sondage.urls', namespace="sondage")),
    
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^traduction/', include ('rosetta.urls')))