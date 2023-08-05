# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import http
from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin

from .models import Redirect
from .utils import get_key_from_path_and_site


class RedirectMiddleware(MiddlewareMixin):

    # Defined as class-level attributes to be subclassing-friendly.
    response_gone_class = http.HttpResponseGone
    response_redirect_class = http.HttpResponseRedirect
    response_permanent_redirect_class = http.HttpResponsePermanentRedirect

    def __init__(self, *args, **kwargs):
        if not apps.is_installed('django.contrib.sites'):
            raise ImproperlyConfigured(
                'You cannot use RedirectFallbackMiddleware when '
                'django.contrib.sites is not installed.'
            )
        super(RedirectMiddleware, self).__init__(*args, **kwargs)

    def do_redirect(self, request, response=None):
        if (
            getattr(settings, 'DJANGOCMS_REDIRECT_404_ONLY', True) and
            response and response.status_code != 404
        ):
            return response

        full_path, part, querystring = request.get_full_path().partition('?')
        querystring = '%s%s' % (part, querystring)
        current_site = get_current_site(request)
        r = None
        key = get_key_from_path_and_site(full_path, settings.SITE_ID)
        cached_redirect = cache.get(key)
        if not cached_redirect:
            try:
                r = Redirect.objects.get(site=current_site, old_path=full_path)
            except Redirect.DoesNotExist:
                pass
            if r is None and not settings.APPEND_SLASH and not request.path.endswith('/'):
                try:
                    r = Redirect.objects.get(
                        site=current_site,
                        old_path=request.get_full_path(force_append_slash=True),
                    )
                except Redirect.DoesNotExist:
                    pass
            cached_redirect = {
                'site': settings.SITE_ID,
                'redirect': r.new_path if r else None,
                'status_code': r.response_code if r else None,
            }
            cache.set(
                key, cached_redirect,
                timeout=getattr(settings, 'DJANGOCMS_REDIRECT_CACHE_TIMEOUT', 3600)
            )
        if cached_redirect['redirect'] == '':
            return self.response_gone_class()
        if cached_redirect['status_code'] == '302':
            return self.response_redirect_class(
                '%s%s' % (cached_redirect['redirect'], querystring)
            )
        elif cached_redirect['status_code'] == '301':
            return self.response_permanent_redirect_class(
                '%s%s' % (cached_redirect['redirect'], querystring)
            )
        elif cached_redirect['status_code'] == '410':
            return self.response_gone_class()

    def process_request(self, request):
        if getattr(settings, 'DJANGOCMS_REDIRECT_USE_REQUEST', True):
            return self.do_redirect(request)

    def process_response(self, request, response):
        redirect = None
        if not getattr(settings, 'DJANGOCMS_REDIRECT_USE_REQUEST', True):
            redirect = self.do_redirect(request, response)
        if redirect:
            return redirect
        return response
