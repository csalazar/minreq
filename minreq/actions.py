import pprint


def print_scrapy_request(results):
    print "Scrapy request\n--------------\n"

    full_url = results['url']
    if 'get_params' in results:
        full_url += '?' + '&'.join(
            ["{0}={1}".format(k, v) for k, v in results['get_params'].items()]
        )

    data = {'url': repr(full_url)}

    data_args = ['cookies', 'headers', 'post_params']
    for da in data_args:
        data[da] = repr(results[da]) if da in results else {}

    get_request = """
    from scrapy.http import Request

    return Request(
        url={url},
        cookies={cookies},
        headers={headers},
        callback='method'
    )
    """

    post_request = """
    from scrapy.http import FormRequest

    return FormRequest(
        url={url},
        formdata={post_params},
        cookies={cookies},
        headers={headers},
        callback='method'
    )
    """

    if results['method'] == 'GET':
        print get_request.format(**data)
    else:
        print post_request.format(**data)


def print_results(results):
    print "Required fields\n---------------\n"
    pprint.pprint(results)
