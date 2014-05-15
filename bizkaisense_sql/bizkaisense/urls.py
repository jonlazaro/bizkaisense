from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bizkaisense.views.home', name='home'),
    # url(r'^bizkaisense/', include('bizkaisense.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'website.views.index'),
    url(r'^station/(?P<stid>\w+)$', 'website.views.station'),
    url(r'^water/(?P<stid>\w+)$', 'website.views.water'),
    url(r'^endpoint$', 'website.views.endpoint'),
    url(r'^docs$', 'website.views.docs'),
    url(r'^api/obs_day/(?P<stid>\w+)/(?P<propid>\w+)/(?P<date>\d{4}\-\d{2}\-\d{2})$', 'website.views.api_obs_day'),
    url(r'^api/outlimit_stations/(?P<propid>\w+)/(?P<startdate>\d{4}\-\d{2}\-\d{2})/(?P<enddate>\d{4}\-\d{2}\-\d{2})/(?P<limit>\d+\.?\d*)$', 'website.views.api_outlimit_stations'),
    url(r'^api/all_stations$', 'website.views.api_all_stations'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    #api/obs_day/EASO/SO2/2011-03-17
)

urlpatterns += staticfiles_urlpatterns()
