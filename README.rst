============================================
django-urli18n
============================================

``django-urli18n`` is a Django reusable app providing only
one thing: showing the currently activated language in the URL.
This is useful for sites you want to have one page in different
languages and accessible via different links according to these
languages (e.g, a News site with article directories in different
languages, ...)

Check it out. It's easy to install and plugs perfectly with Django.

- `0. Introduction`_
- `1. Requirements`_
- `2. Installation`_
- `3. Setup`_
- `4. Usage of the tag or filter`_
- `5. Additional settings`_


.. _introduction: 

0. Introduction
:::::::::::::::::::::::::::::::::::::

Your web-project is multilingual and you want to show different
parts of your site according to which language is chosen? Then 
``django-urli18n`` is the right app for your project. Lets say
you are the owner of example.com and want to to direct users of
different languages to the appropriate pages.

::
    
    http://example.com/de/ -> watch the site in German
    http://example.com/en/ -> watch the site in English
    http://example.com/zh-cn/ -> watch the site in Mandarin Chinese
    

This include all sub pages you include in the configuration for this
app as well. For example if you got a page listing all your articles
of your site:

::
    
    http://example.com/de/articles/ -> watch the article directory in German
    http://example.com/en/articles/ -> watch the article directory in English
    http://example.com/zh-cn/articles/ -> watch the article directory in Mandarin Chinese
    

You don't want to show the language in the URL's path? You can
use a different middleware to show the language in the URL's query
string instead:

::
    
    http://example.com/articles/?lang=de -> watch the article directory in German
    http://example.com/articles/?lang=en -> watch the article directory in English
    http://example.com/articles/?lang=zh-cn -> watch the article directory in Mandarin Chinese
    

**Notes**: 

- ``django-urli18n`` is not used to handle changing the
  language of your site. You need to use other tools which are
  doing this (for example Django's built-in ``set_language`` view
  in ``django.views.i18n`` and Django's built-in middleware class
  ``django.middleware.locale.LocaleMiddleware``).
- in the case you go directly to a page specifing the language in
  the URL (for example to ``http://example.com/de/``)
  ``django-urli18n`` will attempt to change the language, even
  another language was activated before. If you don't specify the
  language in the URL it will attempt to get the language according
  to which way you prefer and then redirect accordingly to the right
  URL. For example if you prefer to use ``django.middleware.locale.LocaleMiddleware``
  it will try to resolve the language from the request and activate it.
  Afterwards ``django-urli18n`` middleware will handle this and
  redirect. 


.. _requirements

1. Requirements
:::::::::::::::::::::::::::::::::::::

At the moment ``django-urli18n`` requires Python_ >2.5 and
Django_ >1.0 to run.


.. _installation

2. Installation
:::::::::::::::::::::::::::::::::::::

Download the source and run:
::
    
    python setup.py install
    


You can also obtain ``django-urli18n`` via PyPi:
    
::
    
    pip install django-urli18n
    
or

::
    
    easy_install django-urli18n
    
 
.. _setup

3. Setup
:::::::::::::::::::::::::::::::::::::

Depending on what you want to achieve you can add one
of the following Middleware classes to your 
``MIDDLEWARE_CLASSES`` setting. Make sure the
Middleware is coming after a Middleware which is activating
the current chosen language, for example Django's built-in
``django.middleware.locale.LocaleMiddleware``.

If you want to display the current language in your URL's
path (for example ``http://example.com/en/home/``)
you should add ``urli18n.middleware.UrlPathTransformMiddleware``:

::
    
    MIDDLEWARE_CLASSES = (
        ...,
        'django.middleware.locale.LocaleMiddleware',
        'urli18n.middleware.UrlPathTransformMiddleware',
    )
    

If you want to display the current language in your URL's query
string (for example ``http://example.com/home/?lang=en``)
you should add ``urli18n.middleware.UrlQuerystringTransformMiddleware``:

::
    
    MIDDLEWARE_CLASSES = (
        ...,
        'django.middleware.locale.LocaleMiddleware',
        'urli18n.middleware.UrlQuerystringTransformMiddleware',
        ...,
    )
    
    
**Note**: Currently it is not possible to add both Middleware's
to the ``MIDDLEWARE_CLASSES`` setting.

This will not automatically transfer all your URL's though. You'll
have to explicitly determine which URL path's are allowed to transform via
the ``URLI18N_INCLUDE_PATHS`` setting. This should be a list
or tuple containing strings or regular expressions of URL path's. You can
simply add some regular expressions from your ``ROOT_URLCONF`` here
and ``django-urli18n`` will handle the rest. For example you could add:

::
    
    URLI18N_INCLUDE_PATHS = ['/', '/home', '^articles/(\d{4})/(\d{2})/$']
    

As you can see there are different ways to actually add an URL path to 
the ``URLI18N_INCLUDE_PATHS`` setting. All of them are valid considering 
a couple facts:
    
- when comparing with the actual path from the request all path's provided 
  will be transformed to start with ``^/`` and end with ``/$``
    
    - something like ``/home`` for example will only match ``^/home/$`` and 
      no other URL path starting with ``/home``
    - use more detailed expressions if you want to match all URL path's following 
      ``/home``, like ``^/home[-\w/]+/$`` for example
      
- Only ``GET`` request's are considered when transforming a url. If you have 
  a view handling a ``POST`` request on a URL path you  provided it will not work. 
  This is simply because it is unnecessary to transform URL path's which are no displayed directly.
- ``MEDIA_URL`` and ``STATIC_URL`` from ``django.conf.settings`` are always 
  excluded even you specify them in ``URLI18N_INCLUDE_PATHS``. 
- If you are using a very general expression like ``'^/.*?/?(?P<slug>[-\w]+)/$`` which 
  is matching anything followed by a slash you might end up transforming all your URL's,
  even you didn't want to. Keep it simple and specify exactly what you want for your
  particular project and you will have no problems. 


You are advised to use the template-tag or template-filter
from ``django-urli18n`` to transform your URL path's directly
in the template. If you are not using them, ``django-urli18n``
will do an extra redirect each time you change to a URL path
provided via ``URLI18N_INCLUDE_PATHS`` in your browser.

To use the template-tag or template-filter add ``urli18n`` to
your ``INSTALLED_APPS``:

::
    
    INSTALLED_APPS = (
        ...,
        'urli18n',
        ...,
    )
    

**Note**: This will also make the app tests available which can be used via
``python manage.py test urli18n``


.. _usage-of-the-tag-or-filter

4. Usage of the tag or filter
:::::::::::::::::::::::::::::::::::::

Most of the things are handled automatically by ``django-urli18n``.
To provide additional control you can use the template tag or template
filter to transform your URL's before they are actually handled by the
middleware. Some examples:

::
    
     <!-- my_template.html -->
     
     {% load urli18n_tags %}
     
     <a href="{% transform_url '/blog/' %}">My blog page</a>
     <a href="{{'/blog/'|transform_url}}">My blog page</a>
     
     {% url my_blog_page_view as blog_url %}
     <a href="{% transform_url blog_url %}">My blog page</a>
     <a href="{{blog_url|transform_url}}">My blog page</a>
     

The ``transform_url`` template tag and filter are doing
exactly the same, except for their syntax in the template.


.. _additional-settings

5. Additional settings
:::::::::::::::::::::::::::::::::::::

There are a couple additional settings you can change to customize
the behavior of ``django-urli18n`` in your project.

``URLI18N_ALWAYS_SHOW_LANGUAGE`` let you determine if
the language shortcut should always be shown in the URL. It defaults
to ``True``. If you don't want to show the language shortcut in your
URL for your default language (defined in Django's ``LANGUAGE_CODE``
setting) you should set this to ``False``:

::
    
    URLI18N_ALWAYS_SHOW_LANGUAGE = False
    

If you are using ``'urli18n.middleware.UrlQuerystringTransformMiddleware'``
to transform your query string instead of your path you can customize the
name of the language parameter in the query string. Simply set 
``URLI18N_QUERYSTRING_NAME``. It defaults to ``'lang'``:

::
    
    URLI18N_QUERYSTRING_NAME = 'my-language'
    




.. _Python: http://www.python.org/
.. _Django: http://www.djangoproject.com/