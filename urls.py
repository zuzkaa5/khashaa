from django.conf.urls import patterns, include, url
from khashaa import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'khashaa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^authenticate/$', views.authenticate, name='authenticate'),
    url(r'^invoice/$', views.invoice, name='invoice'),
    url(r'^check/$', views.check, name='check'),

    url(r'^weburlA/$', views.weburlA, name='weburlA'),
    url(r'^weburlC/$', views.weburlB, name='weburlB'),
    url(r'^weburlB/$', views.weburlC, name='weburlC'),
)
