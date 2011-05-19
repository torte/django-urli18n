# -*- coding: utf-8 -*-

import re
import urlparse

from django.core import exceptions
from django.utils import importlib
from django.utils import translation
from django.conf import settings

from urli18n import app_settings


def show_language(language):
    """Simple helper method to determine if the language
    passed should be shown in the url or not according to 
   `` URLI18N_ALWAYS_SHOW_LANGUAGE`` flag in
    ``app_settings``. 
    
    Params:
        - ``language`` - the language shortcut which should be checked
    
    Returns:
        A Boolean: ``True`` if language should be should, ``False`` otherwise
    """
    return not (app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE is False and language == settings.LANGUAGE_CODE)

def is_included_path(path, strict_mode=True):
    """Helper to determine if a given path should be
    transformed to the show the language in the url. This
    is checked against ``URLI18N_INCLUDE_PATHS`` in 
    ``app_settings``. The ``MEDIA_URL`` and ``STATIC_URL``
    from ``django.conf.settings`` are excluded automatically.
    
    Params:
        - ``path``: the url path which should be checked
        - ``strict_mode``: a boolean which indicates if the path should be checked strict or non-strict. This affects check within the function ``_edit_path_exp`` only.
    
    Returns:
        A Boolean: ``True`` if the given url path should be included,
        ``False`` otherwise.
    """
    path = urlparse.urlparse(path).path
    media_url = getattr(settings, 'MEDIA_URL')
    static_url = getattr(settings, 'STATIC_URL')
    if not (media_url and path.startswith(media_url))\
    and not (static_url and path.startswith(static_url)):
        for p in app_settings.URLI18N_INCLUDE_PATHS:
            p = _edit_path_exp(p, strict_mode)
            regex_path = re.compile(p, re.UNICODE)
            if regex_path.match(path):
                return True
    return False

def _edit_path_exp(path_expression, strict_mode=True):
    """Private helper function transform a regular expression
    given in ``app_settings.URLI18N_INCLUDE_PATHS`` for
    checking. This can be performed in strict or non-strict mode.
    If strict mode it will make sure the given expression ends with
    ``/$``. In non strict mode it will simply not care how the
    expression ends. In both cases it will transform an expression
    to start with ``^/`` though.
    
    Params:
        - ``path_expression``: a regular expression to check against a url path
        - ``strict_mode``: a boolean indicating string or non-strict mode. See explainations above.
        
    Returns:
        - ``path_expression`` (modified if needed)
    """
    if not path_expression.startswith('^/'):
        if path_expression.startswith('^'):
            path_expression = path_expression.replace('^', '^/')
        elif path_expression.startswith('/'):
            path_expression = '^%s' % path_expression
        else:
            path_expression = '^/%s' % path_expression
    if strict_mode is True:
        if not path_expression.endswith('/$'):
            if path_expression.endswith('$'):
                path_expression = path_expression.replace('$', '/$')
            elif path_expression.endswith('/'):
                path_expression = '%s$' % path_expression
            else:
                path_expression = '%s/$' % path_expression
    return path_expression

def process_missing_requests(middleware_object, request):
    """Processes every ``process_request`` method from
    all middleware's which follow this middleware within 
    ``settings.MIDDLEWARE_CLASSES``
    
    Args:
        - ``middleware_object``: the current middleware object
        - ``request``: the current django request object, this will be passed to the ``process_request`` calls
    
    Returns:
        - if a ``process_request`` call returns an HttpResponse it will return this response, else None
    """
    middleware_string = _create_middleware_string(middleware_object)
    middleware_tuple = []
    middleware_appeared = False
    for middleware_path in settings.MIDDLEWARE_CLASSES:
        if middleware_appeared is True:
            middleware_tuple.append(middleware_path)
        if middleware_appeared is False and middleware_path==middleware_string:
            middleware_appeared = True
    middlware_instances = _init_middleware_classes(middleware_tuple)
    for mw_instance in middlware_instances:
        if hasattr(mw_instance, 'process_request'):
            process_result = mw_instance.process_request(request)
            if process_result is not None:
                return process_result
    return None

def process_missing_views(middleware_object, request, view_func, view_args, view_kwargs):
    """Processes every ``process_view`` method from
    all middleware's in ``settings.MIDDLEWARE_CLASSES``.
    Since ``process_view`` calls are never made when calling 
    a view (and returning its response) from a middleware class 
    ``process_request`` method this helper will do the job instead.
    
    Args:
        - ``middleware_object``: the current middleware object
        - ``request``: the current django request object, this will be passed to the ``process_view`` calls
        - ``view_func``: the view function which will be passed to the ``process_view`` calls
        - ``view_args``: the view arguments which will be passed to the ``process_view`` calls
        - ``view_kwargs``: the view keyword arguments which will be passed to the ``process_view`` calls
   
   Returns:
        - if a ``process_view`` call returns an HttpResponse it will return this response, else None
    """
    middlware_instances = _init_middleware_classes(settings.MIDDLEWARE_CLASSES)
    for mw_instance in middlware_instances:
        if hasattr(mw_instance, 'process_view'):
            process_result = mw_instance.process_view(request, view_func, view_args, view_kwargs)
            if process_result is not None:
                return process_result
    return None

def _create_middleware_string(middleware_object):
    """A helper function to provide the string for a
    given middleware object which occur within 
    ``settings.MIDDLEWARE_CLASSES``
    
    Args:
        - ``middleware_object``: the current middleware object
        
    Returns:
        - a string representing the string of the ``middleware_objects`` in ``settings.MIDDLEWARE_CLASSES``
    """
    return  '%s.%s' % (middleware_object.__module__, middleware_object.__class__.__name__)

def _init_middleware_classes(middleware_tuple):
    """A helppr function which initialize all middleware
    classes given by their string representation in a tuple 
    similiar to settings.MIDDLEWARE_CLASSES. Uses the
    same approach as django.core.handlers.base.BaseHandler
    to initialize middleware classes.
    
    Args:
        - ``middleware_tuple``: a tuple of string representations of middleware classes which should be initialized here
        
    Returns:
        - a list of initialized middleware classes
    """
    mw_instances = []
    for middleware_path in middleware_tuple:
        try:
            mw_module, mw_classname = middleware_path.rsplit('.', 1)
        except ValueError:
            raise exceptions.ImproperlyConfigured('%s isn\'t a middleware module' % middleware_path)
        try:
            mod = importlib.import_module(mw_module)
        except ImportError, e:
            raise exceptions.ImproperlyConfigured('Error importing middleware %s: "%s"' % (mw_module, e))
        try:
            mw_class = getattr(mod, mw_classname)
        except AttributeError:
            raise exceptions.ImproperlyConfigured('Middleware module "%s" does not define a "%s" class' % (mw_module, mw_classname))
        try:
            mw_instance = mw_class()
            mw_instances.append(mw_instance)
        except exceptions.MiddlewareNotUsed:
            continue
    return mw_instances

def break_full_path(full_path):
    """Utility function which breaks the full path given from
    django ``request.get_full_path()`` into reasonable bits which can
    be processed by the middleware.
    
    Args:
        - ``full_path``: the full url path from ``request.get_full_path()``
        
    Returns:
        - a tuple containing the following elements:
            - ``path_parts``: the one or two parts of the full_path splitted on the "?"
            - ``querystring_parts``: if querystring was found the querystring parts splitted at the "&", else its an empty list
            - ``language_querystring``: the language querystring determining the current language found in the querystring, if not founded its an empty string
            - ``language_querystring_position``: the index of the language_querystring within ``querystring_parts`` if ``language_querystring`` was found, else None
    """
    querystring_name = app_settings.URLI18N_QUERYSTRING_NAME
    regex_query = re.compile('%s=[-\w]{2,5}' % querystring_name)
    path_parts = full_path.split('?')
    querystring = ''
    querystring_parts = []
    language_querystring_position = None
    language_querystring = ''
    if len(path_parts) > 1:
        querystring = path_parts[1]
        querystring_parts = querystring.split('&')
        for i, part in enumerate(querystring_parts):
            if regex_query.match(part) is not None:
                language_querystring_position = i
                language_querystring = querystring_parts[i]
                break
    return path_parts, querystring_parts, language_querystring, language_querystring_position

def reconstruct_full_path(path, querystring_parts):
    """Utility function which reconstruct the full_path
    according to new paremeters.
    
    Args:
        - ``path``: the absolute path without the querystring
        - ``querystring_parts``: the parts of the querystring as a list, similiar to ``querystring_parts`` from ``break_full_path`` function
    
    Returns:
        - the reconstructed full path with query string
    """
    full_path = path
    if querystring_parts:
        full_path = '?'.join([path, '&'.join(querystring_parts)])
    return full_path

def transform_path(path):
    """Utility function used by the template tags
    to transform given url paths according to active
    language. This helps to change already given urls
    to add the language parameter so the extra 
    redirect within the middleware is not necessary.
    
    Args:
        - ``path``: the url path which should be transformed
        
    Returns:
        - the transformed url path according to which middleware is used and which settings are set
    """
    language = translation.get_language()
    if 'urli18n.middleware.UrlPathTransformMiddleware' in settings.MIDDLEWARE_CLASSES:
        if show_language(language) and not path.startswith('/%s/' % language)\
        and not path=='/%s' % language and is_included_path(path, strict_mode=False):
            path = '/%s%s' % (language, path)
    elif 'urli18n.middleware.UrlQuerystringTransformMiddleware' in settings.MIDDLEWARE_CLASSES:
        if show_language(language) and is_included_path(path, strict_mode=False):
            language_querystring = '%s=%s' % (app_settings.URLI18N_QUERYSTRING_NAME, language)
            path_parts = path.split('?')
            if len(path_parts)==1 or language_querystring not in path_parts[1]:
                if len(path_parts)==1:
                    querystring_parts = []
                else:
                    querystring_parts = path_parts[1].split('&')
                querystring_parts.append(language_querystring)
                path = reconstruct_full_path(path_parts[0], querystring_parts)
    return path

