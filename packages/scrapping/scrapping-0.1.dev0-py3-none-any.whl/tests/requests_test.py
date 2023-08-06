import unittest

import time
import uuid
import requests
from scrapping import requests as req

import logging
logging.basicConfig(level=logging.DEBUG)


class MethodTest(unittest.TestCase):
    def test_function_method(self):
        func = req.Method.function(req.Method.GET)
        self.assertEqual(func, requests.get)

        func = req.Method.function(req.Method.POST)
        self.assertEqual(func, requests.post)


class StatusCodeTest(unittest.TestCase):
    def test_define_response(self):
        status_code = req.StatusCode.define_response(101)
        self.assertEqual(status_code.codes, 100)

        status_code = req.StatusCode.define_response(200)
        self.assertEqual(status_code.codes, 200)

        status_code = req.StatusCode.define_response(301)
        self.assertEqual(status_code.codes, 300)

        status_code = req.StatusCode.define_response(404)
        self.assertEqual(status_code.codes, 400)

        status_code = req.StatusCode.define_response(503)
        self.assertEqual(status_code.codes, 500)


class RequestTest(unittest.TestCase):
    def test_threaded_request(self):
        request = req.Request('https://httpbin.org/')
        self.assertEqual(request._threaded, True)
        self.assertNotEqual(request._thread, None)
        request.join()

    def test_get_request(self):
        value = str(uuid.uuid4())
        request = req.Request('https://httpbin.org/get', parameters={'key': value})
        request.join()
        self.assertIn(value, request.text)

    def test_post_request(self):
        value = str(uuid.uuid4())
        request = req.Request('https://httpbin.org/post', method=req.Method.POST, data={'key': value})
        request.join()
        self.assertIn(value, request.text)

    def test_headers(self):
        request = req.Request('https://httpbin.org/headers', headers={'accept': 'application/json'})
        request.join()
        headers = request.json.get('headers')
        self.assertEqual(headers.get('Accept'), 'application/json')

    def test_user_agent(self):
        request = req.Request('https://httpbin.org/headers', headers={'accept': 'application/json'})
        request.join()
        self.assertEqual(request.user_agent, request._headers.get('User-Agent'))
