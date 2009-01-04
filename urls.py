#coding: utf-8
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

from laws.views import show_laws

urlpatterns = patterns('',
    url(r'skolaar/(?P<schoolyear_starts>\d{4})-(?P<schoolyear_ends>\d{4})/$', show_laws, name = 'laws_show_schoolyear'),
)
