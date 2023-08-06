import requests
import json
import threading
from collections import namedtuple
import contextlib

from urllib.parse import urlparse
from requests import exceptions as ex

from user_agent import generate_user_agent

import logging
logger = logging.getLogger(__name__)

class StatusCode:
    StatusCodeInstance = namedtuple('StatusCodeInstance', 'name codes code', defaults=(None, None, None))
    INFORMATIONAL_RESPONSE = StatusCodeInstance('Informational response', 100)
    SUCCESS = StatusCodeInstance('Success', 200)
    REDIRECTION = StatusCodeInstance('Redirecion', 300)
    CLIENT_ERROR = StatusCodeInstance('Client error', 400)
    SERVER_ERROR = StatusCodeInstance('Server error', 500)

    responses = set((
        INFORMATIONAL_RESPONSE,
        SUCCESS,
        REDIRECTION,
        CLIENT_ERROR,
        SERVER_ERROR,
    ))

    def define_response(status_code):
        if status_code < 100 or status_code > 600:
            return None
        status_code_checker = lambda code_instance: status_code - code_instance.codes >= 0 and status_code - code_instance.codes < 100
        state = list(filter(status_code_checker, StatusCode.responses)).pop()
        return StatusCode.StatusCodeInstance(state.name, state.codes, status_code)


class Method:
    GET = 'GET'
    POST = 'POST'

    def function(method, session=False):
        if method == Method.GET:
            return requests.get if not session else session.get
        elif method == Method.POST:
            return requests.post if not session else session.post


class Request(object):
    def __init__(self, url, parser=None, method=Method.GET, parameters=None, data=None, cookies=None, json=None, headers={}, threaded=True, auto_user_agent=True, timeout=10, verify_ssl=None, use_session=False):
        self._url = url
        self._parameters = parameters
        self._data = data
        self._json = json
        self._headers = headers
        self._method = method
        self._body = None
        self._timeout = timeout
        self._verify_ssl = verify_ssl
        self._threaded = threaded
        self._auto_user_agent = auto_user_agent
        self._use_session = use_session
        self._thread = None

        self.parser = parser
        self.parsed_url = urlparse(self._url)
        self.name = self.parsed_url.netloc + self.parsed_url.path
        self.ready = False
        self.error = None
        self.cookies = cookies
        self.user_agent = generate_user_agent() if self._auto_user_agent else None
        self._headers.update({'User-Agent': self.user_agent})
        self.session = requests.Session() if self._use_session else None
        self.response = None
        self.text = ''
        self.json = None

        self.logger = logger

        if self._threaded:
            self.logger.debug('The request is set to threaded')
            self._create_request_thread()
            self._start_threaded_request()

    def __repr__(self):
        if self._threaded:
            threaded = "Threaded"
            if self.response:
                response = self.response.status_code
            else: response = "running"
        else:
            threaded = ""
            response = "not defined"
        return "<{threaded} {method} Request to {url} . Response [{response}]>".format(threaded=threaded, method=self._method, url=self._url, response=response)

    def send_request(self):
        method = Method.function(self._method, session=self.session)
        try:
            self.response = method(
                self._url, data=self._data, params=self._parameters, headers=self._headers, json=self._json, cookies=self.cookies, timeout=self._timeout, verify=self._verify_ssl,
            )
        except ex.RequestException as e:
            self.error = e
            self.ready = True
            return

        self.text = self.response.text
        with contextlib.suppress(json.decoder.JSONDecodeError):
            self.json = self.response.json()
        self.cookies = self.response.cookies.get_dict()
        self.status = StatusCode.define_response(self.response.status_code)

        self.logger.debug("[{}] Request with status {}".format(self.name, self.status))
        self.ready = True

    def join(self):
        while not self.ready:
            pass

    @property
    def status_exception(self):
        try:
            self.response.raise_for_status()
        except ex.RequestException as exception:
            return exception

    def _create_request_thread(self):
        self.logger.debug('Building thread for {}...'.format(self.name))
        self._thread = threading.Thread(target=self.send_request)


    def _start_threaded_request(self):
        self.logger.debug('Starting thread for {}...'.format(self.name))
        self._thread.start()
        self.logger.debug('Thread for {} running'.format(self.name))
