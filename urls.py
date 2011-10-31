from django.conf.urls.defaults import *
from authz.views import AuthorizorView
from authz.models import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.register(Authorizer)
admin.site.register(Resource)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'postgres1.views.home', name='home'),
    # url(r'^postgres1/', include('postgres1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authorize/$', AuthorizorView.as_view(), name='CompanyTree'),
)
