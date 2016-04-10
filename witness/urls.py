# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'witness.views.home', name='home'),
    url(r'^document/(?P<document_slug>[-\w]+)/(?P<version_number>[-\.\w]+)/$',
        'witness.views.document_detail', name='document_detail'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='auth_logout'),
    # BrowserID
    (r'^browserid/', include('django_browserid.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the flatpages:
    ('^pages/', include('django.contrib.flatpages.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^{0!s}/(?P<path>.*)$'.format(media_url), 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
