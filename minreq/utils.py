import re


def get_cookie_key(headers):
    """ Return cookie key used by the site """
    for k in headers.keys():
        if re.search('cookie', k, flags=re.I):
            return k
    else:
        return None
