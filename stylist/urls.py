from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stylist.views.home', name='home'),
    # url(r'^stylist/', include('stylist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^grades/', include(admin.site.urls)),
    url(r'^cpplint/submit', 'cpplint.views.submit'),
    url(r'^cpplint/upload', 'cpplint.views.upload'),
    url(r'^cpplint/invalid', 'cpplint.views.invalid'),
    url(r'^cpplint/', 'cpplint.views.submit'),
)
