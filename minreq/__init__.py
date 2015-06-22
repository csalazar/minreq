#!/usr/bin/env python
import requests
import re
import md5

from copy import deepcopy


class ParsingError(Exception):
    pass


def parse_curl_request(curl_request):
    try:
        url = re.findall("curl '(.*?)'", curl_request)[0]
    except IndexError:
        raise ParsingError('Invalid url')

    #Dictionary of headers valid for requests library
    raw_headers = re.findall("-H '(.*?):\s(.*?)'", curl_request)
    headers = {k: v for k, v in raw_headers}

    return (url, headers)


def strip_cookie_content(url, expected_md5, headers, cookie_content):
    cookie_values = cookie_content.split(';')
    required_values = []
    deleted_values = []
    print '[+] Starting deep cookie inspection.'

    for value in cookie_values:
        print '[?] Stripping value %s' % value
        deleted_values.append(value)

        headers['Cookie'] = ';'.join(
            [v for v in cookie_values if v not in deleted_values]
        )
        r = requests.get(url, headers=headers)
        request_md5 = md5.new(r.content).hexdigest()

        if request_md5 != expected_md5:
            print '[+] Value %s is necessary.' % value
            required_values.append(value)
            deleted_values.pop()

    return ';'.join(required_values)


def main():
    curl_request = raw_input()
    url, headers = parse_curl_request(curl_request)

    #Getting md5 of expected response
    r = requests.get(url, headers=headers)
    expected_md5 = md5.new(r.content).hexdigest()

    #Start checking for required headers
    required_headers = {}
    for header_name, header_value in headers.items():
        print '[?] Requesting without header %s' % header_name

        request_headers = {k: v for k, v in headers.items() if k != header_name}
        r = requests.get(url, headers=request_headers)
        request_md5 = md5.new(r.content).hexdigest()

        if request_md5 != expected_md5:
            print '[+] Header %s is necessary.' % header_name
            if header_name == 'Cookie':
                header_value = strip_cookie_content(
                    url, expected_md5, deepcopy(headers), header_value
                )
            required_headers.update({header_name: header_value})

    print required_headers

if __name__ == '__main__':
    main()
