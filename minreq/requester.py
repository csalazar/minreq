from collections import namedtuple

import requests

from .utils import get_cookie_key

from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class Requester():
    def __init__(self, curl_data, differ, debug):
        self.data = curl_data
        self.cookie_key = get_cookie_key(self.data.headers)
        self.debug = debug

        self.differ = differ(response=self._get_original_response())

    def requester(self, *a, **kw):
        if self.data.method == 'POST':
            return requests.post(*a, **kw)
        else:
            return requests.get(*a, **kw)

    def _build_url(self, params=None):
        if not params:
            return self.data.url

        return "%s?%s" % (
            self.data.clean_url,
            '&'.join(["{0}={1}".format(k, v) for k, v in params.items()])
        )

    def build_request(self, headers=None, cookies=None, get_params=None, post_params=None):
        if not headers:
            headers = self.data.headers

        #Get rid of cookie header if custom cookies are provided
        if cookies:
            try:
                del headers[self.cookie_key]
            except:
                pass

        if not get_params:
            get_params = self.data.params['get']

        if not post_params:
            post_params = self.data.params['post']

        url = self._build_url(get_params)

        return self.requester(
            url=url,
            cookies=cookies,
            headers=headers,
            data=post_params
        )

    def _get_original_response(self):
        r = self.build_request()
        return r.text

    def determine_required_params(self, test):
        required_params = {}

        for param, value in test.param_dict.items():
            new_params = {k: v for k, v in test.param_dict.items() if k != param}

            request = self.build_request(**{test.arg_name: new_params})
            response = request.text

            if self.differ.is_param_required(response):
                if self.debug:
                    print "[+] Parameter '%s' is required." % param

                required_params[param] = value

        return required_params

    def get_results_from_comparison(self):
        required_data = {
            'url': self.data.clean_url,
            'method': self.data.method
        }

        Test = namedtuple('Test', ['arg_name', 'param_dict'])
        necessary_tests = [
            Test('get_params', self.data.params['get']),
            Test('post_params', self.data.params['post']),
            Test('headers', self.data.headers),
        ]
        cookie_test = Test('cookies', self.data.cookies)

        #Test every group of fields except cookies
        for t in necessary_tests:
            required_params = self.determine_required_params(t)
            if required_params:
                required_data[t.arg_name] = required_params

        #Do cookie testing if cookie is a required header
        if required_data.get('headers', {}).get(self.cookie_key, False):
            if self.debug:
                print '[+] Doing cookie inspection ..'

            required_params = self.determine_required_params(cookie_test)

            if required_params:
                required_data[cookie_test.arg_name] = required_params

                #Delete cookie header since cookies are in ``required_data['cookies']`` dict
                del required_data['headers'][self.cookie_key]

        return required_data
