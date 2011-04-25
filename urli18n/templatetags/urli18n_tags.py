# -*- coding: utf-8 -*-

from django import template

from urli18n import utils


register = template.Library()

def transform_url(path):
    """Transforms the url path according to
    acitivated Middleware. See ``urli18n.utils.transform_path``
    for more information.
    """
    return utils.transform_path(path)
register.simple_tag(transform_url)

def transform_url_filter(path):
    """Transforms the url path according to
    acitivated Middleware. See ``urli18n.utils.transform_path``
    for more information.
    """
    return utils.transform_path(path)
register.filter('transform_url', transform_url_filter)
        
