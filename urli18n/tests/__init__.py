# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import translation
from django.conf import settings

from urli18n import app_settings
from urli18n.templatetags import urli18n_tags


class UrlPathTransformMiddlewareTestCase(TestCase):
    urls = 'urli18n.tests.urls'
    
    def setUp(self):
        self.curr_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        self.curr_LANGUAGE_CODE = settings.LANGUAGE_CODE
        self.curr_LANGUAGES = settings.LANGUAGES
        self.curr_app_URLI18N_INCLUDE_PATHS = app_settings.URLI18N_INCLUDE_PATHS
        self.curr_app_URLI18N_ALWAYS_SHOW_LANGUAGE = app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE
        settings.MIDDLEWARE_CLASSES = (
            'urli18n.middleware.UrlPathTransformMiddleware',
        )
        settings.LANGUAGE_CODE = 'en'
        settings.LANGUAGES = (
            ('de', 'Deutsch'),
            ('en', 'English'),
            ('zh-cn', '中文'),
        )
        self.included_paths = ['/', '/home', '^articles/(\d{4})/(\d{2})/$', 
                               '^/articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$']
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
    
    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.curr_MIDDLEWARE_CLASSES
        settings.LANGUAGE_CODE = self.curr_LANGUAGE_CODE
        settings.LANGUAGES = self.curr_LANGUAGES
        app_settings.URLI18N_INCLUDE_PATHS = self.curr_app_URLI18N_INCLUDE_PATHS
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = self.curr_app_URLI18N_ALWAYS_SHOW_LANGUAGE

    def test_view1_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/')
        self.assertRedirects(response, '/en/')
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view1_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/')
        self.assertRedirects(response, '/de/')
        response = self.client.get('/de/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view1_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/')
        self.assertRedirects(response, '/zh-cn/')
        response = self.client.get('/zh-cn/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view2_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/home/')
        self.assertRedirects(response, '/en/home/')
        response = self.client.get('/en/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view2_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/home/')
        self.assertRedirects(response, '/de/home/')
        response = self.client.get('/de/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view2_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/home/')
        self.assertRedirects(response, '/zh-cn/home/')
        response = self.client.get('/zh-cn/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view3_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/articles/2011/01/')
        self.assertRedirects(response, '/en/articles/2011/01/')
        response = self.client.get('/en/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.content, '2011-01')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.content, '2011-01')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.content, '2011-01')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view3_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/articles/2011/01/')
        self.assertRedirects(response, '/de/articles/2011/01/')
        response = self.client.get('/de/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.content, '2011-01')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.content, '2011-01')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view3_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/articles/2011/01/')
        self.assertRedirects(response, '/zh-cn/articles/2011/01/')
        response = self.client.get('/zh-cn/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.content, '2011-01')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.content, '2011-01')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view4_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/articles/2011/02/28/')
        self.assertRedirects(response, '/en/articles/2011/02/28/')
        response = self.client.get('/en/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.content, '2011-02-28')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.content, '2011-02-28')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.content, '2011-02-28')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view4_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/articles/2011/02/28/')
        self.assertRedirects(response, '/de/articles/2011/02/28/')
        response = self.client.get('/de/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.content, '2011-02-28')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.content, '2011-02-28')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view4_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/articles/2011/02/28/')
        self.assertRedirects(response, '/zh-cn/articles/2011/02/28/')
        response = self.client.get('/zh-cn/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.content, '2011-02-28')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.content, '2011-02-28')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_direct_to_url(self):
        translation.activate(settings.LANGUAGE_CODE)
        response = self.client.get('/de/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        response = self.client.get('/zh-cn/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        
    def test_template_tag(self):
        translation.activate('en')
        path = urli18n_tags.transform_url('/')
        self.assertEqual(path, '/en/')
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/en/home')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/en/home/?param=true')
        path = urli18n_tags.transform_url('/en/home/')
        self.assertEqual(path, '/en/home/')
        path = urli18n_tags.transform_url('/en')
        self.assertEqual(path, '/en')
        #change the default behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        path = urli18n_tags.transform_url('/')
        self.assertEqual(path, '/')
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url('/en/home/')
        self.assertEqual(path, '/en/home/')
        path = urli18n_tags.transform_url('/en')
        self.assertEqual(path, '/en')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url('/home/')
        self.assertEqual(path, '/home/')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        #activate a different language
        translation.activate('zh-cn')
        path = urli18n_tags.transform_url('/')
        self.assertEqual(path, '/zh-cn/')
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/zh-cn/home')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/zh-cn/home/?param=true')
        path = urli18n_tags.transform_url('/zh-cn/home/')
        self.assertEqual(path, '/zh-cn/home/')
        path = urli18n_tags.transform_url('/zh-cn')
        self.assertEqual(path, '/zh-cn')
        
    def test_template_filter(self):
        translation.activate('en')
        path = urli18n_tags.transform_url_filter('/')
        self.assertEqual(path, '/en/')
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/en/home')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/en/home/?param=true')
        path = urli18n_tags.transform_url_filter('/en/home/')
        self.assertEqual(path, '/en/home/')
        path = urli18n_tags.transform_url('/en')
        self.assertEqual(path, '/en')
        #change the default behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        path = urli18n_tags.transform_url_filter('/')
        self.assertEqual(path, '/')
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url_filter('/en/home/')
        self.assertEqual(path, '/en/home/')
        path = urli18n_tags.transform_url('/en')
        self.assertEqual(path, '/en')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url_filter('/home/')
        self.assertEqual(path, '/home/')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        #activate a different language
        translation.activate('zh-cn')
        path = urli18n_tags.transform_url_filter('/')
        self.assertEqual(path, '/zh-cn/')
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/zh-cn/home')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/zh-cn/home/?param=true')
        path = urli18n_tags.transform_url_filter('/zh-cn/home/')
        self.assertEqual(path, '/zh-cn/home/')
        path = urli18n_tags.transform_url_filter('/zh-cn')
        self.assertEqual(path, '/zh-cn')
        
        
class UrlQuerystringTransformMiddlewareTestCase(TestCase):
    urls = 'urli18n.tests.urls'
    
    def setUp(self):
        self.curr_MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES
        self.curr_LANGUAGE_CODE = settings.LANGUAGE_CODE
        self.curr_LANGUAGES = settings.LANGUAGES
        self.curr_app_URLI18N_INCLUDE_PATHS = app_settings.URLI18N_INCLUDE_PATHS
        self.curr_app_URLI18N_ALWAYS_SHOW_LANGUAGE = app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE
        settings.MIDDLEWARE_CLASSES = (
            'urli18n.middleware.UrlQuerystringTransformMiddleware',
        )
        settings.LANGUAGE_CODE = 'en'
        settings.LANGUAGES = (
            ('de', 'Deutsch'),
            ('en', 'English'),
            ('zh-cn', '中文'),
        )
        self.included_paths = ['/', 'home/', '^articles/(\d{4})/(\d{2})/$', 
                               '^/articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/$']
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_QUERYSTRING_NAME = 'lang'
    
    def tearDown(self):
        settings.MIDDLEWARE_CLASSES = self.curr_MIDDLEWARE_CLASSES
        settings.LANGUAGE_CODE = self.curr_LANGUAGE_CODE
        settings.LANGUAGES = self.curr_LANGUAGES
        app_settings.URLI18N_INCLUDE_PATHS = self.curr_app_URLI18N_INCLUDE_PATHS
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = self.curr_app_URLI18N_ALWAYS_SHOW_LANGUAGE
    
    def test_view1_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/')
        self.assertRedirects(response, '/?lang=en')
        response = self.client.get('/?lang=en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=en')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view1_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/')
        self.assertRedirects(response, '/?lang=de')
        response = self.client.get('/?lang=de')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=de')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view1_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/')
        self.assertRedirects(response, '/?lang=zh-cn')
        response = self.client.get('/?lang=zh-cn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=zh-cn')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view2_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/home/')
        self.assertRedirects(response, '/home/?lang=en')
        response = self.client.get('/home/?lang=en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=en')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view2_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/home/')
        self.assertRedirects(response, '/home/?lang=de')
        response = self.client.get('/home/?lang=de')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=de')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view2_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/home/')
        self.assertRedirects(response, '/home/?lang=zh-cn')
        response = self.client.get('/home/?lang=zh-cn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=zh-cn')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view3_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/articles/2011/01/')
        self.assertRedirects(response, '/articles/2011/01/?lang=en')
        response = self.client.get('/articles/2011/01/?lang=en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=en')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view3_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/articles/2011/01/')
        self.assertRedirects(response, '/articles/2011/01/?lang=de')
        response = self.client.get('/articles/2011/01/?lang=de')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=de')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view3_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/articles/2011/01/')
        self.assertRedirects(response, '/articles/2011/01/?lang=zh-cn')
        response = self.client.get('/articles/2011/01/?lang=zh-cn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=zh-cn')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/01/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view4_en(self):
        #first with standard settings
        translation.activate('en')
        response = self.client.get('/articles/2011/02/28/')
        self.assertRedirects(response, '/articles/2011/02/28/?lang=en')
        response = self.client.get('/articles/2011/02/28/?lang=en')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=en')
        #change the standard behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view4_de(self):
        #first with standard settings
        translation.activate('de')
        response = self.client.get('/articles/2011/02/28/')
        self.assertRedirects(response, '/articles/2011/02/28/?lang=de')
        response = self.client.get('/articles/2011/02/28/?lang=de')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=de')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_view4_zhcn(self):
        #first with standard settings
        translation.activate('zh-cn')
        response = self.client.get('/articles/2011/02/28/')
        self.assertRedirects(response, '/articles/2011/02/28/?lang=zh-cn')
        response = self.client.get('/articles/2011/02/28/?lang=zh-cn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=zh-cn')
        #exclude the url 
        app_settings.URLI18N_INCLUDE_PATHS = []
        response = self.client.get('/articles/2011/02/28/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], '')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        
    def test_direct_to_url(self):
        translation.activate(settings.LANGUAGE_CODE)
        response = self.client.get('/home/?lang=de')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=de')
        response = self.client.get('/home/?lang=zh-cn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=zh-cn')
        
    def test_with_additional_params(self):
        translation.activate(settings.LANGUAGE_CODE)
        response = self.client.get('/home/?lang=de&web=django')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'de')
        self.assertEqual(response.request['QUERY_STRING'], 'lang=de&web=django')
        response = self.client.get('/home/?param=test&lang=zh-cn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'zh-cn')
        self.assertEqual(response.request['QUERY_STRING'], 'param=test&lang=zh-cn')
        response = self.client.get('/home/?param=test&lang=en&web=django')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.request['QUERY_STRING'], 'param=test&lang=en&web=django')
       
    def test_template_tag(self):
        translation.activate('en')
        path = urli18n_tags.transform_url('/')
        self.assertEqual(path, '/?lang=en')
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/home?lang=en')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/home/?param=true&lang=en')
        path = urli18n_tags.transform_url('/home/?lang=en')
        self.assertEqual(path, '/home/?lang=en')
        path = urli18n_tags.transform_url('/?lang=en')
        self.assertEqual(path, '/?lang=en')
        #change the default behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        path = urli18n_tags.transform_url('/')
        self.assertEqual(path, '/')
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url('/en/home/')
        self.assertEqual(path, '/en/home/')
        path = urli18n_tags.transform_url('/en')
        self.assertEqual(path, '/en')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url('/home/')
        self.assertEqual(path, '/home/')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        #activate a different language
        translation.activate('zh-cn')
        path = urli18n_tags.transform_url('/')
        self.assertEqual(path, '/?lang=zh-cn')
        path = urli18n_tags.transform_url('/home')
        self.assertEqual(path, '/home?lang=zh-cn')
        path = urli18n_tags.transform_url('/home/?param=true')
        self.assertEqual(path, '/home/?param=true&lang=zh-cn')
        path = urli18n_tags.transform_url('/home/?lang=zh-cn')
        self.assertEqual(path, '/home/?lang=zh-cn')
        path = urli18n_tags.transform_url('/?lang=zh-cn')
        self.assertEqual(path, '/?lang=zh-cn')
        
    def test_template_filter(self):
        translation.activate('en')
        path = urli18n_tags.transform_url_filter('/')
        self.assertEqual(path, '/?lang=en')
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/home?lang=en')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/home/?param=true&lang=en')
        path = urli18n_tags.transform_url_filter('/home/?lang=en')
        self.assertEqual(path, '/home/?lang=en')
        path = urli18n_tags.transform_url_filter('/?lang=en')
        self.assertEqual(path, '/?lang=en')
        #change the default behavior
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = False
        path = urli18n_tags.transform_url_filter('/')
        self.assertEqual(path, '/')
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url_filter('/en/home/')
        self.assertEqual(path, '/en/home/')
        path = urli18n_tags.transform_url_filter('/en')
        self.assertEqual(path, '/en')
        #exclude the url 
        app_settings.URLI18N_ALWAYS_SHOW_LANGUAGE = True
        app_settings.URLI18N_INCLUDE_PATHS = []
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/home')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/home/?param=true')
        path = urli18n_tags.transform_url_filter('/home/')
        self.assertEqual(path, '/home/')
        app_settings.URLI18N_INCLUDE_PATHS = self.included_paths
        #activate a different language
        translation.activate('zh-cn')
        path = urli18n_tags.transform_url_filter('/')
        self.assertEqual(path, '/?lang=zh-cn')
        path = urli18n_tags.transform_url_filter('/home')
        self.assertEqual(path, '/home?lang=zh-cn')
        path = urli18n_tags.transform_url_filter('/home/?param=true')
        self.assertEqual(path, '/home/?param=true&lang=zh-cn')
        path = urli18n_tags.transform_url_filter('/home/?lang=zh-cn')
        self.assertEqual(path, '/home/?lang=zh-cn')
        path = urli18n_tags.transform_url_filter('/?lang=zh-cn')
        self.assertEqual(path, '/?lang=zh-cn')
        
