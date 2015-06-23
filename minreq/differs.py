import hashlib


class MD5Differ(object):
    def __init__(self, response):
        self.original_response = response
        self.original_response_md5 = self._get_md5_sum(response)

    def _get_md5_sum(self, response):
        md5 = hashlib.md5()
        md5.update(response.encode('utf-8'))
        return md5.hexdigest()

    def is_param_required(self, response):
        response_md5 = self._get_md5_sum(response)
        if response_md5 != self.original_response_md5:
            return True
        else:
            return False
