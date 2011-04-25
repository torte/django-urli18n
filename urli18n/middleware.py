# -*- coding: utf-8 -*-

import re

from django.utils import translation
from django.core import urlresolvers
from django import http
from django import shortcuts
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from urli18n import utils
from urli18n import app_settings


class UrlPathTransformMiddleware(object):
    """A django middleware class which transforms
    the url path according to the current activated language.
    For example if current activated language is German the
    root url might look something like this:
    
    ``http://example.com/de/``
    
    If your url path was for example /home/myblog/ the
    path will be transformed to this:
    
    ``http://example.com/de/home/myblog/``
    
    This middleware also detects of a language is already given
    in the url at the beginning ot the path and if so does not
    attempt to transform the url/redirect to the new location.
    """
    
    def process_request(self, request):
        """Process the request of according to following conditions:
        
        - Only processes ``GET`` request, since others will not be displayed in the address bar anyway
        - Only processes ``GET`` request for url path's (as regular expressions) which are provided in ``URLI18N_INCLUDE_PATHS`` setting. If a path is provided in ``URLI18N_INCLUDE_PATHS`` setting it will transform the url, for all others the url will not be transformed (though the language will be changed)
        - If the url path does not start with a language prefix and it will build a new url from given path and redirect to it 
        - If ``URLI18N_ALWAYS_SHOW_LANGUAGE`` setting is set to True (the default) it will always show the language prefix in the url, if  ``URLI18N_ALWAYS_SHOW_LANGUAGE`` setting is set to False it will show the language prefix only for languages which are not the default language (set via the django setting for ``LANGUAGE_CODE``)
        - If url path starts with a valid language prefix it will render the view attached to the given url in the original url conf. If will resolve other middleware classes ``process_request`` and ``process_view`` calls first to avoid conflicts
        - If user is not navigating on the page but coming from a source which is not the domain of this project it will change the language directly when provided in the url or if not provided use the current activated language (given by process_request of django.middleware.locale.LocaleMiddleware)
        
        Args:
            - ``request``: the django request object to process
            
        Returns:
            - Either a redirect response to the right path with leading language shortcut or the view response for the view attached to the url of the path
        """
        if request.method == 'GET':
            path = request.path
            full_path = request.get_full_path()
            language = translation.get_language()
            host = request.get_host()
            redirect_to = None
            regex_ref = re.compile('^http[s]?://%s' % host, re.UNICODE)
            referer = request.META.get('HTTP_REFERER', None)
            language_shortcuts = [lang[0] for lang in settings.LANGUAGES]
            if utils.is_included_path(path) and utils.show_language(language):
                #redirect to the url with the appropriate language shortcut
                return shortcuts.redirect('/%s%s' % (language, full_path))
            regex_prefix = re.compile('^/[-\w]+/')
            language_from_path = regex_prefix.findall(path)
            if language_from_path:
                language_from_path = language_from_path[0].replace('/','')
                if not referer or regex_ref.match(referer) is None:
                    if language_from_path in language_shortcuts and language_from_path!=language:
                        translation.activate(language_from_path)
                        request.LANGUAGE_CODE = translation.get_language()
                        language = translation.get_language()
                if language_from_path in language_shortcuts and language_from_path!=language:
                    #cut of the language shortcut
                    path = path.replace('/%s' % language_from_path, '', 1)
                    full_path = full_path.replace('/%s' % language_from_path, '', 1)
                    #check if the path is_included_path
                    if utils.is_included_path(path):
                        #redirect to the url with the appropriate language shortcut
                        if utils.show_language(language):
                            return shortcuts.redirect('/%s%s' % (language, full_path))
                        else:
                            return shortcuts.redirect('%s' % full_path)
                elif language_from_path==language and utils.show_language(language):
                    path = path.replace('/%s' % language_from_path, '', 1)
                    full_path = full_path.replace('/%s' % language_from_path, '', 1)
                    #check if the path is_included_path
                    if utils.is_included_path(path):
                        #render the view
                        #all the other middleware's following this middleware in
                        #settings MIDDLEWARE_CLASSES still need to be
                        #processed (process_request) + all Middleware's inside
                        #of settings MIDDLEWARE_CLASSES process_view
                        #methods need to be processed as well before actually
                        #returning the view here
                        view, args, kwargs = urlresolvers.resolve(path)
                        process_request_result = utils.process_missing_requests(self, request)
                        if process_request_result is not None:
                            return process_request_result
                        process_request_view = utils.process_missing_views(self, request, view, args, kwargs)
                        if process_request_view is not None:
                            return process_request_view
                        return view(request, *args, **kwargs)
            

class UrlQuerystringTransformMiddleware(object):
    """A django middleware class which transforms
    the url's query string according to the current activated language.
    For example if current activated language is German the
    root url might look something like this:
    
    ``http://example.com/?lang=de``
    
    If your url path was for example /home/myblog/ the
    path will be transformed to this:
    
    ``http://example.com/home/myblog/?lang=de``
    
    You can also add other parameters to the query string
    without changing the bahviour:
    
    ``http://example.com/?param=1&lang=de``
    
    This middleware also detects of a language is already given
    in the url at the beginning ot the path and if so does not
    attempt to transform the url/redirect to the new location.
    """
    
    def process_request(self, request):
        """Process the request of according to following conditions:
        
        - Only processes ``GET`` request, since others will not be displayed in the address bar anyway
        - Only processes ``GET`` request for url path's which are not provided in ``URLI18N_EXCLUDE_PATHS`` setting. If a path is provided in ``URLI18N_EXCLUDE_PATHS`` setting it will simply not transform the url (though change the language)
        - If the url query string does not include the language parameter it will build a new url from given path and query string and redirect to it 
        - If ``URLI18N_ALWAYS_SHOW_LANGUAGE`` setting is set to ``True`` (the default) it will always show the language in the query string, if  ``URLI18N_ALWAYS_SHOW_LANGUAGE`` setting is set to ``False`` it will show the language query string only for languages which are not the default language (set via the django setting for ``LANGUAGE_CODE``)
        - If user is not navigating on the page but coming from a source which is not the domain of this project it will change the language directly when provided in the url or if not provided use the current activated language (given by process_request of django.middleware.locale.LocaleMiddleware)
        
        Args:
            - ``request``: the django request object to process
            
        Returns:
            - Either a redirect response to the right path with leading language shortcut or the view response for the view attached to the url of the path
        """
        path = request.path_info
        if request.method == 'GET' and utils.is_included_path(path):
            full_path = request.get_full_path()
            querystring_name = app_settings.URLI18N_QUERYSTRING_NAME
            
            path_parts, querystring_parts, language_querystring, language_querystring_position = utils.break_full_path(full_path)
            
            language = translation.get_language()
            host = request.get_host()
            redirect_to = None
            regex_ref = re.compile('^http[s]?://%s' % host, re.UNICODE)
            referer = request.META.get('HTTP_REFERER', None)
            language_shortcuts = [lang[0] for lang in settings.LANGUAGES]
            
            if not referer or regex_ref.match(referer) is None and language_querystring:
                #change the language according to the path if
                #its provided in the path, else try to use the
                #last activated language
                language_from_querystring = language_querystring.replace('%s=' % querystring_name,'')
                if language_from_querystring in language_shortcuts:
                    translation.activate(language_from_querystring)
                    request.LANGUAGE_CODE = translation.get_language()
                    language = translation.get_language()
            
            #reconstruct the language_querystring
            language_querystring = '%s=%s' % (querystring_name, language)
            
            if app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE is False\
            and settings.LANGUAGE_CODE == language:
                #dont' rewrite urls for the default language if setting is set
                if language_querystring_position is not None:
                    querystring_parts.pop(language_querystring_position)
                    full_path = utils.reconstruct_full_path(path_parts[0], querystring_parts)
                if full_path != request.get_full_path():
                    return shortcuts.redirect(full_path)
            else:
                if language_querystring_position is not None\
                and language_querystring != querystring_parts[language_querystring_position]:
                    querystring_parts[language_querystring_position] = language_querystring
                    redirect_to = utils.reconstruct_full_path(path_parts[0], querystring_parts)
                elif language_querystring_position is None:
                    querystring_parts.append(language_querystring)
                    redirect_to = utils.reconstruct_full_path(path_parts[0], querystring_parts)
                if redirect_to is not None:
                    return shortcuts.redirect(redirect_to)

        
