import requests

KHIPU_BASE_ENDPOINT = 'https://khipu.com/api/{version}'
CONTENT_TYPE = 'application/x-www-form-urlencoded'
AUTHORIZED_HTTP_METHODS = ['get', 'post', 'delete']
KHIPU_HEADER = {
    'Authorization': '',
    'Content-Type': '%s' % CONTENT_TYPE,
}
API_METHODS = {
    'get': lambda config: requests.get(**config),
    'post': lambda config: requests.post(**config),
    'delete': lambda config:  requests.delete(**config),
}
