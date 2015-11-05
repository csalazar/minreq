minreq
======

Check required data in a request.

Usage
-----

Some time ago Chrome Developers tools added `Copy as
Curl <https://twitter.com/ChromiumDev/status/317183238026186752>`_ feature.
This tool receives as input a curl command, parses it and
checks what data is required to repeat the request successfully.
It currently supports `GET` and `POST` requests.

The output depends on the action,
which are currently `print_results` and `print_scrapy_request`.
An example using the latest one is shown below:


.. code:: python

  $ python minreq-runner.py --action print_scrapy_request
  curl 'https://en.wikipedia.org/w/load.php?debug=false&lang=en&modules=startup&only=scripts&skin=vector&*'
  -H 'accept-encoding: gzip, deflate, sdch' -H 'accept-language: en-US,en;q=0.8,es;q=0.6'
  -H 'user-agent: Mozilla/5.0' -H 'accept: */*' -H 'referer: https://en.wikipedia.org/wiki/Example'
  -H 'cookie: GeoIP=:::::v6; WMF-Last-Access=23-Jun-2015' --compressed


  Scrapy request
  --------------


  from scrapy.http import Request

  return Request(
      url='https://en.wikipedia.org/w/load.php?only=scripts&modules=startup',
      cookies={},
      headers={},
      callback='method'
  )
