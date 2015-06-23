#!/usr/bin/env python
import re

from collections import namedtuple

from .utils import get_cookie_key


def splitter(s, delimiter):
    """ Split ``s`` with ``delimiter`` and then split substrings with key=value logic.

        :rtype: dict

    """
    tuples = []
    for substring in s.split(delimiter):
        substring = substring.strip()

        data = re.split('\s*=\s*', substring, maxsplit=1)
        if len(data) == 2:
            tuples.append(re.split('\s*=\s*', substring, maxsplit=1))

    return dict(tuples)


class CurlDataGetter(object):
    CurlData = namedtuple(
        'CurlData', ['url', 'clean_url', 'method', 'headers', 'cookies', 'params']
    )

    def __init__(self, curl_request):
        self.curl_request = curl_request

    def get_url(self, without_params=False):
        """ Return URL

            :returns: URL
            :rtype: str

        """
        full_url = re.findall("curl '(.*?)'\s", self.curl_request)[0]
        if without_params:
            return re.sub('\?.*', '', self.get_url())
        else:
            return full_url

    def get_method(self):
        """ Return request method, currently tested GET and POST.

            :returns: 'POST' or 'GET'
            :rtype: str

        """
        if re.search("'\s--data\s'", self.curl_request):
            return 'POST'
        else:
            return 'GET'

    def get_headers(self):
        """ Return headers after extracting them from ``self.curl_request``.

            :returns: headers keys and values
            :rtype: dict

        """
        raw_headers = re.findall("-H '(.*?):\s(.*?)'", self.curl_request)
        return {k: v for k, v in raw_headers}

    def get_cookies(self, cookie_header):
        """ Return cookies after extracting them from cookie header.

            :returns: cookies keys and values
            :rtype: dict

        """
        if not cookie_header:
            return {}

        return splitter(cookie_header, ';')

    def get_get_params(self, url):
        """ Return GET params extracted from url.

            :returns: get params keys and values
            :rtype: dict

        """
        param_string = re.findall('\?(.*)', url)
        if not param_string:
            return {}

        return splitter(param_string[0], '&')

    def get_post_params(self):
        """ Return POST params extracted from --data string.

            :returns: params keys and values
            :rtype: dict

        """
        data_string = re.findall("'\s--data\s'(.*?)'\s", self.curl_request)
        if not data_string:
            return {}

        return splitter(data_string[0], '&')

    def get_data(self):
        data = {}

        data['url'] = self.get_url()
        data['clean_url'] = self.get_url(without_params=True)
        data['method'] = self.get_method()
        data['headers'] = self.get_headers()

        try:
            cookies = data['headers'][get_cookie_key(data['headers'])]
        except:
            cookies = ''

        data['cookies'] = self.get_cookies(cookies)

        data['params'] = {}
        data['params']['get'] = self.get_get_params(data['url'])
        data['params']['post'] = self.get_post_params()

        return self.CurlData(**data)
