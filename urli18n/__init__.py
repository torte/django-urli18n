# -*- coding: utf-8 -*-

from django.core import exceptions
from django.conf import settings

from urli18n import utils
from urli18n import app_settings


if not isinstance(app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE, bool):
    raise exceptions.ImproperlyConfigured('URLI18N_ALWAYS_SHOW_LANGUAGE need to be set to a boolean value.')
if not isinstance(app_settings.URLI18N_INCLUDE_PATHS, (list, tuple)):
    raise exceptions.ImproperlyConfigured('URLI18N_INCLUDE_PATHS need to be a list or tuple.')
    for element in app_settings.URLI18N_INCLUDE_PATHS:
        if not isinstance(element, (str, unicode)):
            raise exceptions.ImproperlyConfigured('All elements in URLI18N_INCLUDE_PATHS need to be set to a str or unicode.')
if not isinstance(app_settings.URLI18N_QUERYSTRING_NAME, (str, unicode)):
    raise exceptions.ImproperlyConfigured('URLI18N_QUERYSTRING_NAME need to be set to a str or unicode value.')

if 'urli18n.middleware.UrlPathTransformMiddleware' in settings.MIDDLEWARE_CLASSES\
and 'urli18n.middleware.UrlQuerystringTransformMiddleware' in settings.MIDDLEWARE_CLASSES:
    raise exceptions.ImproperlyConfigured('Only one of the middleware classes provided by urli18n can be used in settings.MIDDLEWARE_CLASSES.')
