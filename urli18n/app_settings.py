# -*- coding: utf-8 -*-

from django.conf import settings

"""Set this setting if you want to change the behavior
when a language is shown in the url or not. If set to True
(the default) it will always show the language shortcut/query-string 
in the url according to the middleware which is used. If set to False
it will not show the language shortcut/query-string for the default language
which is given by LANGUAGE_CODE setting in django
settings.
"""
URLI18N_ALWAYS_SHOW_LANGUAGE = getattr(settings, 'URLI18N_ALWAYS_SHOW_LANGUAGE', True)

"""This need to be a list or tuple containing strings or regular expressions
of url path's which should be included by the middleware. If included
the url will be modified when using the url path provided here.

If you use a string or regular expression to provide a path make sure 
its starts with a leading slash  ("/..." or "^/..."), since it will only check for
absolute urls starting from your url root (which is usually just "/"). 
If you not add a leading "^/" to your strings the middleware will handle
it though and add this to the start of the reg exp string when comparing
with the actual path. The same goes for path's which are not ending with
``/$``. The middleware will add a trailing ``/$``.
"""
URLI18N_INCLUDE_PATHS = getattr(settings, 'URLI18N_INCLUDE_PATHS', [])

"""Only need to set this if you use 
``'urli18n.middleware.UrlQuerystringTransformMiddleware'``
in your settings.MIDDLEWARE_CLASSES.
This need to be a string representing the name of the 
language key in the query-string. It defaults to 'lang'.
"""
URLI18N_QUERYSTRING_NAME = getattr(settings, 'URLI18N_QUERYSTRING_NAME', 'lang')
