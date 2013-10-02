minreq
======

Check required headers in a request.

Usage
-----

Some time ago Chrome Developers tools added "[Copy as
Curl](https://twitter.com/ChromiumDev/status/317183238026186752)" feature.
This script receives as input a curl command, parses it and returns only
required headers from the request in order to be valid and successful.

The output is a python dictionary, helpful for emulating requests in frameworks
like scrapy.
