from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^cpplint/upload', 'cpplint.views.upload'),
    url(r'^cpplint/invalid', 'cpplint.views.invalid'),
    url(r'^cpplint/', 'cpplint.views.upload'),
)
