from .call_api import call_api
from .settings import KHIPU_BASE_ENDPOINT


class Khipupy:
    def __init__(self, receiver_id, secret, base_url=None, version='2.0'):
        self.receiver_id = receiver_id
        self.secret = secret
        self.version = version
        self.base_url = KHIPU_BASE_ENDPOINT.format(version=self.version)

    def banks(self):

        return call_api(
            url=self.base_url,
            secret=self.secret,
            receiver_id=self.receiver_id,
            extra='/banks',
        )

    def payments(self, data={}, service='', method='post'):

        return call_api(
            url=self.base_url,
            method=method,
            data=data,
            secret=self.secret,
            receiver_id=self.receiver_id,
            extra='/payments%s' % service,
        )

    def receivers(self, data={}):

        return call_api(
            url=self.base_url,
            method='post',
            data=data,
            secret=self.secret,
            receiver_id=self.receiver_id,
            extra='/receivers',
        )
