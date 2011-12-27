from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.base import TemplateView
from app.views import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'postgres1.views.home', name='home'),
    # url(r'^postgres1/', include('postgres1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^access/$', AccessView.as_view(), name='access'),
    url(r'^qr/$', QRGenView.as_view(), name='qrgen'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authorize/$', AuthorizorView.as_view(), name='Authorize'),
    url(r'^upload/$', CertUploadView.as_view(), name='CertUpload'),
    url(r'^register/$', RegisterView.as_view(), name='Register'),
    url(r'^log/(.+)/$', LogView.as_view(), name='Log'),
    url(r'^scan/$', ScanView.as_view(), name='Scan'),
)

