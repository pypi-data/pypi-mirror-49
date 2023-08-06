# -*- coding: utf-8 -*-
"""monkey patch"""
import logging.config
import traceback
import copy

from httplog import settings


def patch_httplib2():
    try:
        import httplib2
        from httplog.support.httplib2 import Http
        httplib2.Http = Http
    except ImportError:
        pass
    except Exception:
        traceback.print_exc()


def patch_requests():
    try:
        import requests
        from httplog.support.requests import Session
        requests.sessions.Session = Session
        requests.Session = Session
    except ImportError:
        pass
    except Exception:
        traceback.print_exc()


def patch_urlopen():
    try:
        import urllib2
        from httplog.support.urllib2 import http_log_wraper
        urllib2.urlopen = http_log_wraper(urllib2.urlopen)
    except Exception:
        traceback.print_exc()


def monkey_patch(httplib2=True, requests=True, urlopen=True, logfile='', logformat=''):
    # 设置logging
    log_conf = copy.deepcopy(settings.LOGGING)
    if logfile:
        # 使用文件
        log_conf['loggers']['httplog']['handlers'] = ['file']
        settings.FILE['filename'] = logfile
        log_conf['handlers']['file'] = settings.FILE

    if logformat:
        log_conf['formatters']['simple']['format'] = logformat
    logging.config.dictConfig(log_conf)

    if httplib2:
        patch_httplib2()
    if requests:
        patch_requests()
    if urlopen:
        patch_urlopen()
