from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'story_share.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^story_site/', include('story_site.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
