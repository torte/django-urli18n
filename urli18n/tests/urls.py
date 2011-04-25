# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'urli18n.tests.views.view1'),
    url(r'^home/$', 'urli18n.tests.views.view2'),
    url(r'^articles/(\d{4})/(\d{2})/$', 'urli18n.tests.views.view3'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$', 'urli18n.tests.views.view4'),
)