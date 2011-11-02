from django.conf.urls.defaults import *
from django.conf import settings
from authz.views import AuthorizorView, CertUploadView, RegisterView
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'postgres1.views.home', name='home'),
    # url(r'^postgres1/', include('postgres1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authorize/$', AuthorizorView.as_view(), name='Authorize'),
    url(r'^upload/$', CertUploadView.as_view(), name='CertUpload'),
    url(r'^register/$', RegisterView.as_view(), name='Register'),
)

# For local dev server only
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )