from unittest import TestCase
from minreq.curl import CurlDataGetter


class TestCurlDataGetter(TestCase):
    def test_get_url(self):
        #Test valid cases
        url_with_params = 'http://domain.tld/?var=1'
        url_without_params = 'http://domain.tld/'

        cdg = CurlDataGetter("curl '%s' datadatadata" % url_with_params)
        self.assertEqual(url_without_params, cdg.get_url(without_params=True))
        self.assertEqual(url_with_params, cdg.get_url())

        cdg = CurlDataGetter("curl '%s' datadatadata" % url_without_params)
        self.assertEqual(url_without_params, cdg.get_url(without_params=True))
        self.assertEqual(url_without_params, cdg.get_url())

    def test_get_method(self):
        cdg = CurlDataGetter("curl 'http://domain.tld' -H 'bla' --data 'param'")
        self.assertEqual('POST', cdg.get_method())

        cdg = CurlDataGetter("curl 'http://domain.tld' -H 'bla'")
        self.assertEqual('GET', cdg.get_method())

    def test_get_headers(self):
        cdg = CurlDataGetter("curl 'http://domain.tld' -H 'A: 1' -H 'B: 2'")
        self.assertEqual({'A': '1', 'B': '2'}, cdg.get_headers())

    def test_get_cookies(self):
        cdg = CurlDataGetter("curl 'http://domain.tld'")
        self.assertEqual({'A': '1', 'B': '2'}, cdg.get_cookies('A=1; B=2'))

    def test_get_get_params(self):
        cdg = CurlDataGetter("curl 'http://domain.tld?A=1&B=2' -H")
        url = cdg.get_url()
        self.assertEqual({'A': '1', 'B': '2'}, cdg.get_get_params(url))

        cdg = CurlDataGetter("curl 'http://domain.tld' -H")
        url = cdg.get_url()
        self.assertEqual({}, cdg.get_get_params(url))

    def test_get_post_params(self):
        cdg = CurlDataGetter("curl 'http://domain.tld' --data 'A=1&B=2' -H")
        self.assertEqual({'A': '1', 'B': '2'}, cdg.get_post_params())

        cdg = CurlDataGetter("curl 'http://domain.tld' -H")
        self.assertEqual({}, cdg.get_post_params())
